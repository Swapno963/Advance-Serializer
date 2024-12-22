# Advance-Serializers
## Done
1. Work with nested searilizer
2. Work with nested selrilizer
7. Field-Level Custom Validation
9. Serializer Relations
10. Using SerializerMethodField

## Pending
3. Serializer Inheritance
  - Basic Inheritance
4. Custom to_representation Method
5. Custom create and update Methods
6. Dynamic Fields Serializer

8. Serializer-Level Validation
Use specific fields for relationships:
 - PrimaryKeyRelatedField
 - SlugRelatedField
 - HyperlinkedRelatedField
 - StringRelatedField

11. Polymorphic Serializers
12. Validation Using Third-Party Libraries
Leverage libraries like django-rest-framework-json-schema or drf-flex-fields for JSON schema validation and dynamic field selection.
12. Custom Fields
 - Create custom fields for non-standard data types or formats.
```python
class CommaSeparatedListField(serializers.Field):
    def to_representation(self, value):
        return ",".join(value)

    def to_internal_value(self, data):
        return data.split(",")

class CustomSerializer(serializers.Serializer):
    tags = CommaSeparatedListField()

```
13. Output Formats (JSON, XML, etc.)
 - Customize output by overriding renderers in the view.
```python
from rest_framework.renderers import JSONRenderer, XMLRenderer

class CustomViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer, XMLRenderer]

```
14. Integrating Serializers with ViewSets and QuerySets
- Use multiple serializers for different actions:
```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListProductSerializer
        if self.action == 'retrieve':
            return DetailedProductSerializer
        return DefaultProductSerializer
```
