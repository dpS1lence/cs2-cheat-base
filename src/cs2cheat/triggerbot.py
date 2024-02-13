# trigger_bot.py
import pymem
import pymem.process
import keyboard
import time
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
from random import uniform
import threading
from offsets import *


class TriggerBot(threading.Thread):
    def __init__(self, trigger_key="shift"):
        threading.Thread.__init__(self)
        self.trigger_key = trigger_key
        self.mouse = Controller()
        self.client = Client()
        self.pm = pymem.Pymem("cs2.exe")
        self.client_module = pymem.process.module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll

        self.dwEntityList = self.client.offset('dwEntityList')
        self.dwLocalPlayerPawn = self.client.offset('dwLocalPlayerPawn')
        self.dwViewMatrix = self.client.offset('dwViewMatrix')

        self.dwForceAttack = self.client.offset('dwForceAttack')
        self.dwForceJump = self.client.offset('dwForceJump')

        self.m_iTeamNum = self.client.get('C_BaseEntity', 'm_iTeamNum')
        self.m_iHealth = self.client.get('C_BaseEntity', 'm_iHealth')
        self.m_fFlags = self.client.get('C_BaseEntity', 'm_fFlags')
        self.m_bSpotted = self.client.get('EntitySpottedState_t', 'm_bSpotted')
        self.x = self.client.get('C_LocalTempEntity', 'x')
        self.y = self.client.get('C_LocalTempEntity', 'y')

        self.m_iIDEntIndex = self.client.get('C_CSPlayerPawnBase', 'm_iIDEntIndex')
        self.m_vecViewOffset = self.client.get('C_BaseModelEntity', 'm_vecViewOffset')
        self.running = True

    def run(self):
        print(f"[-] TriggerBot started.\n[-] Trigger key: {self.trigger_key.upper()}")
        while self.running:
            try:
                if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                    continue

                if keyboard.is_pressed(self.trigger_key):
                    self.trigger_action()
                else:
                    self.trigger_action()
            except KeyboardInterrupt:
                self.stop()

    @staticmethod
    def read_vector3(pm, address):
        """
        Reads a Vector3 from memory, assuming a structure of three consecutive floats.

        Args:
            pm: The Pymem instance used to read memory.
            address: The memory address where the Vector3 starts.

        Returns:
            A tuple of (x, y, z) representing the Vector3 read from memory.
        """
        x = pm.read_float(address)
        y = pm.read_float(address + 4)  # Assuming a float is 4 bytes
        z = pm.read_float(address + 8)
        return x, y, z

    def trigger_action(self):
        player = self.pm.read_longlong(self.client_module + self.dwLocalPlayerPawn)
        entity_id = self.pm.read_int(player + self.m_iIDEntIndex)

        if entity_id > 0:
            ent_list = self.pm.read_longlong(self.client_module + self.dwEntityList)

            #self.read_entities_position()

            ent_entry = self.pm.read_longlong(ent_list + 0x8 * (entity_id >> 9) + 0x10)
            entity = self.pm.read_longlong(ent_entry + 120 * (entity_id & 0x1FF))

            entity_team = self.pm.read_int(entity + self.m_iTeamNum)
            player_team = self.pm.read_int(player + self.m_iTeamNum)

            if entity_team != player_team:
                entity_hp = self.pm.read_int(entity + self.m_iHealth)
                if entity_hp > 0:
                    time.sleep(uniform(0.01, 0.03))
                    self.mouse.press(Button.left)
                    time.sleep(uniform(0.01, 0.05))
                    self.mouse.release(Button.left)
        pass

    def read_entities_position(self):
        for i in range(1, 64):
            entity_address = self.pm.read_int(
                self.client_module + self.dwEntityList + i * 0x10)  # Assuming entity stride of 0x10
            if entity_address:
                # Example: Reading X, Y, Z position of the entity. Adjust the offsets based on your game's structure.
                # This is a simplified example. The actual structure and offsets will vary.
                vec = entity_address + self.m_vecViewOffset
                vec_view_offset = TriggerBot.read_vector3(self.pm, vec)
                print(f"View Offset: {i} X={vec_view_offset[0]}, Y={vec_view_offset[1]}, Z={vec_view_offset[2]}")

    def stop(self):
        self.running = False
