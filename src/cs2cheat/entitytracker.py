import threading
import time


class EntityTracker(threading.Thread):
    def __init__(self, pymem_instance, client_module_base, entity_base_address):
        threading.Thread.__init__(self)
        self.pm = pymem_instance
        self.client_module_base = client_module_base
        self.entity_base_address = entity_base_address
        self.running = True  # Control the running of the thread

    def run(self):
        while self.running:
            self.print_entity_position()
            time.sleep(1)  # Adjust the sleep time as needed

    def print_entity_position(self):
        highest_entity_index = self.pm.read_int(
            self.client_module_base + self.dwGameEntitySystem + self.entity_count_offset)
        for i in range(highest_entity_index):
            entity_address = self.pm.read_int(
                self.client_module_base + self.dwEntityList + i * 0x10)  # Assuming entity stride of 0x10
            if entity_address:
                # Example: Reading X, Y, Z position of the entity. Adjust the offsets based on your game's structure.
                # This is a simplified example. The actual structure and offsets will vary.
                x = self.pm.read_float(entity_address + 0x000)  # Placeholder offset for X
                y = self.pm.read_float(entity_address + 0x004)  # Placeholder offset for Y
                z = self.pm.read_float(entity_address + 0x008)  # Placeholder offset for Z
                print(f"Entity {i}: X={x}, Y={y}, Z={z}")

    def stop(self):
        self.running = False

