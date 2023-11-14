from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class MenuItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название пункта")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родитель",
    )
    path = models.CharField(max_length=255, blank=True, editable=True)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def get_absolute_url(self):
        return reverse(
            "detail",
            kwargs={
                "path": self.path,
            },
        )

    @classmethod
    def get_menu_data(cls, obj_title:str =None):
        if obj_title is None:
            return ""
        query = f"""
            WITH RECURSIVE MenuCTE AS (
                SELECT id, title, parent_id, path, 1 AS level
                FROM menu_tree_menuitem
                WHERE title = %s
                UNION ALL
                SELECT child.id, child.title, child.parent_id, child.path, MenuCTE.level - 1
                FROM MenuCTE
                JOIN menu_tree_menuitem child ON MenuCTE.id = child.parent_id
                WHERE MenuCTE.level = 1
                UNION ALL
                SELECT parent.id, parent.title, parent.parent_id, parent.path, MenuCTE.level + 1
                FROM MenuCTE
                JOIN menu_tree_menuitem parent ON MenuCTE.parent_id = parent.id
                WHERE MenuCTE.level > 0
            )
            SELECT * FROM MenuCTE
            ORDER BY id;
        """
        menu_data = cls.objects.raw(query, [obj_title])
        return menu_data

    def _get_all_parents(self) -> str:
        """Сплит self.path на идентификаторы для дальнейшего получения предков и потомков.
        Преобразование в строку для удоства работы с SQL"""
        splitted_path = self.path.split("/")
        parents_list_str = ", ".join(map(str, splitted_path))
        if parents_list_str:
            return parents_list_str
        return ''

    def __str__(self):
        return self.title


@receiver(post_save, sender=MenuItem)
def set_path_on_save(sender, instance, **kwargs):
    """Устанавливает значение поля 'path' после сохранения экземпляра,
    если оно отсутствует. Путь формируется на основе наличия родителя"""
    if not instance.path:
        if instance.parent:
            instance.path = f"{instance.parent.path}/{instance.id}"
        else:
            instance.path = str(instance.id)
        instance.save()