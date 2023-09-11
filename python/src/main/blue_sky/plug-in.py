# Import BlueSky objects
from bluesky import core

# Initialization function of your plugin
def init_plugin():

    config = {
        # The name of your plugin
        'plugin_name': 'SamplePlugin',

        # The type of this plugin
        'plugin_type': 'sim'
    }

    # Initialize and return the configuration dict
    return config

# Example new entity object for BlueSky
class SampleEntity(core.Entity):
    def __init__(self):
        super().__init__()

    def update(self, aircraft):
        # Example functionality: Print the aircraft's ID
        print(f"Aircraft {aircraft.id} is updated by SampleEntity.")

# Instantiate the SampleEntity and use it to create an instance
# of your plugin.
sample_entity = SampleEntity()

# Define the main update function for your plugin
def update_plugin(aircraft):
    # Call the update method of the SampleEntity
    sample_entity.update(aircraft)

# Register your plugin's update function with BlueSky
core.register(update_plugin)
