from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from blog.models import Post, Comment
from blog.helpers import count_words, read_time


User = get_user_model()


image_path = "static/images/read.jpg"


class PostModelTest(TestCase):
    """
    Test the Post Model
    """
    def setUp(self):
        user = User.objects.create_superuser(
            email="admin@email.com",
            first_name="Admin",
            last_name="Root",
            password="admin"
        )
        post_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=(open(image_path, 'rb').read()),
            content_type="image/jpeg"
        )
        self.post = Post.objects.create(
            title="Article title",
            body="Artice Test content",
            image=post_image,
            author=user
        )

    def test_str_representation(self):
        """
        Test the __str__ method of the post
        :return:
        """
        self.assertEqual(self.post.__str__(), self.post.status)

    def test_auto_populate_updated_date(self):
        """
        Test whether the updated_date field of the post is prepopulated
        :return:
        """
        self.assertIsNotNone(self.post.updated_date)

        prev_post_updated_date = self.post.updated_date
        self.post.body = 'New Post Body'
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.updated_date > prev_post_updated_date)

    def test_get_absolute_url(self):
        """
        Test for absolute url of an article (detail_post)
        :return:
        """
        expected_url = reverse(
            "blog:post_detail", args=[
                self.post.published_date.year,
                self.post.published_date.month,
                self.post.published_date.day,
                self.post.slug
            ]
        )
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_get_delete_url(self):
        """
        Test for delete url of an article
        :return:
        """
        expected_url = reverse(
            "blog:post_delete", args=[
                self.post.published_date.year,
                self.post.published_date.month,
                self.post.published_date.day,
                self.post.slug
            ]
        )
        self.assertTrue(self.post.get_delete_url(), expected_url)

    def test_words_count(self):
        """
        Test for the number of words of an article
        :return:
        """
        expected_words = count_words(self.post.body)
        self.assertEqual(self.post.words_count, expected_words)

    def test_read_duration(self):
        """
        Test for the total duration(time) used for reading an article
        :return:
        """
        expected_read_time = read_time(self.post.body)
        self.assertEqual(self.post.read_duration, expected_read_time)


class PostCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            email="admin@email.com",
            first_name="Admin",
            last_name="Root",
            password="admin"
        )
        post_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=(open(image_path, 'rb').read()),
            content_type="image/jpeg"
        )
        cls.post = Post.objects.create(
            title="Article title",
            body="Artice Test content",
            image=post_image,
            author=cls.user
        )

    def setUp(self):
        self.post_comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            body="Sample Comment"
        )

    def test_str_representation(self):
        """
        Test the __str__ method that it returns 'Comment by {author full name} on {post}
        :return:
        """
        expected_representation = f"Comment by {self.user.full_name()} on {self.post}"
        # import pdb; pdb.set_trace()
        self.assertEqual(self.post_comment.__str__(), expected_representation)

    def test_author_related_name(self):
        """
        TODO: Will provide implementation
        Test the related name for the ManyToOne Relation to author
        :return:
        """
        pass

    def test_post_related_name(self):
        """
        TODO: Will provide implementation
        Test the related name for the ManyToOne Relation to post
        :return:
        """
        pass
