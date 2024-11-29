from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)

    def add_user(self, user: User) -> None:  # type: ignore
        if user in self.members.all():
            raise ValueError("User already exists in the group!")

        self.members.add(user)
        self.save()
        return

    def remove_user(self, user: User) -> None:  # type: ignore
        if user not in self.members.all():
            raise ValueError("User is not a member of the group!")
        self.members.remove(user)
        self.save()
        return

    def __str__(self) -> str:
        return f"Group {uuid}"


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField()
    time_stamped = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message by {self.author} in group {self.group}"
