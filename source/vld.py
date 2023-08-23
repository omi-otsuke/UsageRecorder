import wx


class ValueExistsValidator(wx.Validator):
    def __init__(self, label_name):
        wx.Validator.__init__(self)
        self.label_name = label_name

    def Clone(self):
        return ValueExistsValidator(self.label_name)

    def Validate(self, win):
        control = self.GetWindow()
        if len(control.GetValue().strip()) == 0:
            return False
        else:
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class AtLeastOneValidator(wx.Validator):
    def __init__(self, checkboxes, label_name):
        super(AtLeastOneValidator, self).__init__()
        self.checkboxes = checkboxes
        self.label_name = label_name

    def Clone(self):
        return AtLeastOneValidator(self.checkboxes, self.label_name)

    def Validate(self, win):
        return any(checkbox.IsChecked() for checkbox in self.checkboxes)

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
