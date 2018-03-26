class User(object):
  def __init__(self, first_name, last_name, email, password, salt, birthdate, permission_level):
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.password = password
      self.birthdate = birthdate
      self.permission_level

  def sell(self):
      self.status = "Sold"
      return self

  def addTax(self, tax):
      print "Sale price: ${}.".format(self.price * (1 + (1 * tax)))
      return self

  def Return(self, reason):
      lreason = reason.lower()
      if lreason == "defective":
	self.status = lreason
	self.price = 0
      elif lreason == "in box, like new":
	self.status = "For Sale"
      elif lreason == "box open":
	self.status = "used"
	self.price -= (self.price * .2)
      return self

  def display_info(self):
      print "Name: {}, Price: ${}, Weight: {}lbs., Brand: {}, Status: {}".format(self.name, self.price, self.weight, self.brand, self.status)
      return self

#vacuum = Product(200, "Tornado", 25, "Bissel")
#vacuum.addTax(.13).sell().display_info().Return("Box Open").display_info()
