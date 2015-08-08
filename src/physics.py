class Physics():
  def __init__(self):
    self.x_vel = 0

    self.y_vel = 0
    self.old_y_vel = 0

    self.grav = 0.5
    self.air_resistance = 0.5

    self.fall = True
    self.old_fall = True


  def physics_update(self):
    if self.fall:
      self.old_y_vel = self.y_vel
      self.y_vel += self.grav
    else:
      self.old_y_vel = self.y_vel
      self.y_vel = 0

    if abs(self.x_vel) < self.air_resistance:
      self.x_vel = 0.0
    else:
      if self.x_vel > 0:
        self.x_vel -= self.air_resistance
      else:
        self.x_vel += self.air_resistance
