

class SoundSequence:
    """
    Play a fixed sound sequence.
    """
    def __init__(self, duration_time: float, running: bool, sounds):
        self.sound_index = 0
        self.delay = duration_time
        self.duration_time = duration_time
        self.running = running
        self.sounds = []
        for sound in sounds:
            self.sounds.append(sound)
        self.sequences_length = len(self.sounds)

    def set_volume(self, volume: float):
        for sound in self.sounds:
                sound.set_volume(volume)

    def set_duration(self, new_duration_time):
        if self.duration_time != new_duration_time:
            self.duration_time = new_duration_time
            self.reset()

    def reset(self):
        self.sound_index = 0
        self.delay = self.duration_time

    def update(self, delta_time):
        if self.running:
            self.delay += delta_time
            if self.delay > self.duration_time:
                selected = self.sounds[self.sound_index]
                selected.play()
                self.sound_index = (self.sound_index + 1) % self.sequences_length
                self.delay = 0.0

    def start(self):
        """Start sequence"""
        self.reset()
        self.running = True

    def stop(self):
        """Stop sequence when last sound is played"""
        self.running = False

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True
