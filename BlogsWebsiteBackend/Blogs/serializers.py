from rest_framework import serializers

from .base.serializers import Base64ImageField
from .models import Post, PostImage, Category, HashTag
import logging

logger = logging.getLogger('main')


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    name = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = PostImage
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=True, read_only=True, required=False)
    category_id = serializers.PrimaryKeyRelatedField(many=True, read_only=False, required=False,
                                                     queryset=Category.objects.all(), source='category')
    hash_tag = HashTagSerializer(many=True, required=False)
    image = ImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'url', 'author', 'title', 'status', 'publication_date',
                  'context', 'category_id', 'category', 'image', 'hash_tag')
        read_only_fields = ('publication_date', 'author')

    def create(self, validated_data):
        logger.info('Starting creation of a new post!')
        user = self.context['request'].user

        status = validated_data.pop('status', 'NULL')
        hash_tags = validated_data.pop('hash_tag', [])
        photos = validated_data.pop('image', [])
        category = validated_data.pop('category', [])

        if user.is_staff:
            validated_data['status'] = status
        else:
            validated_data['status'] = 'NULL'

        post_instance = Post.objects.create(**validated_data)
        post_instance.category.add(*category)

        for hash_tag in hash_tags:
            HashTag.objects.create(post=post_instance, **hash_tag)
        for photo in photos:
            PostImage.objects.create(post=post_instance, **photo)
        return post_instance

    @staticmethod
    def _nested_update_fk(instance, data, model):
        fields_with_same_post_instance = model.objects.filter(post=instance.pk)

        fields_id_pool = []

        for field in data:
            if "id" in field.keys():
                logger.info('Updating an existing data!')
                if model.objects.filter(id=field['id']).exists() and \
                        field['id'] in fields_with_same_post_instance.values_list('id', flat=True):
                    field_instance = model.objects.get(id=field['id'])
                    field_instance.name = field.get('name', field_instance.name)
                    field_instance.save()
                    fields_id_pool.append(field_instance.id)
                else:
                    continue
            else:
                logger.info('Adding a new data!')
                model_instance = model.objects.create(post=instance, **field)
                fields_id_pool.append(model_instance.id)

        for field in fields_with_same_post_instance:
            logger.info('Deleting the data which value is "None".')
            if field.name == "None":
                model.objects.filter(pk=field.id).delete()

    def update(self, instance, validated_data):
        logger.info(f'Starting an update of a post {instance.id}!')
        user = self.context['request'].user
        if user.is_staff:
            instance.status = validated_data.get('status', instance.status)
        hash_tags = validated_data.pop('hash_tag', [])
        images = validated_data.pop('image', [])
        categories = validated_data.pop('category_id', [])
        instance.title = validated_data.get('title', instance.title)
        instance.context = validated_data.get('context', instance.context)

        if categories:
            logger.info('Adding categories!')
            instance.category.clear()
            instance.category.add(*categories)
        instance.save()

        logger.info('Adding hash tags!')
        self._nested_update_fk(instance, hash_tags, HashTag)
        logger.info('Adding images!')
        self._nested_update_fk(instance, images, PostImage)

        return instance
