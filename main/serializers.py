from rest_framework import serializers

from .models import Problem, CodeImage, Reply, Comment

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(),
                                                   many=True).data
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(),
                                                        many=True).data
        return representation


    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        print(request.user)
        problem = Problem.objects.create(
            author=request.user,
            **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image,
                                     problem=problem)
        return problem


    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(
                image=image,
                problem=instance
            )
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Reply
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(
                instance.comments.all(), many=True
            ).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment




