from rest_framework import serializers
from .models import *


class BasicProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
        ]
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
    
    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "stock must be greater than 0."
            )
        return value


class ProductSerializer( BasicProductSerializer):
    class Meta:
        model = Product
        fields = BasicProductSerializer.Meta.fields


    

class DetailedUserSerializer(BasicProductSerializer):
    extra_field = serializers.SerializerMethodField()

    class Meta(BasicProductSerializer.Meta):
        fields = BasicProductSerializer.Meta.fields + ['extra_field', 'price','stock'] 

    def get_extra_field(self, obj):
        return f"Extra info for {obj.name}"
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )


class CommaSeparatedListField(serializers.Field):
    def to_representation(self, value):
        # Convert the list to a comma-separated string
        return " ".join(value)

    def to_internal_value(self, data):
        # Convert the comma-separated string to a list
        return data.split(",")
    # pass


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    tags = CommaSeparatedListField()


    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["custom_field"] = "Custom Value"
        return data



class BaseProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()

class PhysicalProductSerializer(BaseProductSerializer):
    weight = serializers.FloatField()
    dimensions = serializers.CharField(max_length=100)

class DigitalProductSerializer(BaseProductSerializer):
    file_size = serializers.FloatField()
    download_url = serializers.URLField()

class ProductPolymorphicSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    def get_type(self, obj):
        if isinstance(obj, PhysicalProduct):
            return "physical"
        elif isinstance(obj, DigitalProduct):
            return "digital"
        return "unknown"

    def get_product(self, obj):
        if isinstance(obj, PhysicalProduct):
            return PhysicalProductSerializer(obj).data
        elif isinstance(obj, DigitalProduct):
            return DigitalProductSerializer(obj).data
        return {}

    def to_representation(self, obj):
        """
        Customize the representation to include the type field at the root level.
        """
        data = super().to_representation(obj)
        return {"type": data["type"], "product": data["product"]}
