from lnst.Controller import Controller, HostReq, DeviceReq, BaseRecipe

class HelloWorldRecipe(BaseRecipe):
    machine1 = HostReq()
    machine1.nic1 = DeviceReq(label = "net1")
    