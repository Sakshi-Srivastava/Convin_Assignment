

from django.db import models
from django.db import models
from model_utils import FieldTracker

class SimpleTrackedModel(models.Model):
    """Simple model with tracked name"""

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
    tracker = FieldTracker(fields=['name'])
"""Field tracker tests"""

from django.test import TestCase

from test_app.models import SimpleTrackedModel

class GenericTrackerTest(TestCase):
    """Test generic tracker"""

    def setUp(self):
        """Performs per-test initialization"""

        self.instance: SimpleTrackedModel = SimpleTrackedModel.objects.create(name='Old name')

    def test_refresh_from_db(self):
        """Test tracker after untracked update() and refresh_from_db()"""

        old_name = self.instance.name
        new_name = 'New name'

        # Call update(), nothing changed locally (as expected)
        updated: int = SimpleTrackedModel.objects.filter(pk=self.instance.pk).update(name=new_name)
        self.assertEqual(updated, 1)
        self.assertEqual(self.instance.name, old_name)
        self.assertDictEqual(self.instance.tracker.changed(), {})

        # refresh_from_db(), and now we have changes (even though save() won't change anything)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, new_name)
        self.assertDictEqual(self.instance.tracker.changed(), {'name': 'Old name'})

        # If we re-set the value, the tracker doesn't show changes even though this would be a change
        self.instance.name = old_name
        self.assertDictEqual(self.instance.tracker.changed(), {})

        # To get this to work, we have to refresh_from_db() and then save!
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, new_name)
        self.instance.save()
        self.instance.name = old_name

        self.assertDictEqual(self.instance.tracker.changed(), {'name': 'New name'})
        
 
