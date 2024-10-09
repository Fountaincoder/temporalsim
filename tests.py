"""temporal simulation test suite"""

import unittest
from temporalunit import *
from temporallib import *


class SimpleTest(unittest.TestCase):
    """ test suite"""
    A2 = "00001010000000"
    A3 = "00100001000000"
    c1 = "0010010"
    b1 = 0b10100100
    c2 = "001001"
    b2 = 0b1100100
    c3 = "01"
    b3 = 0b101
    c4 = "0"

    def test1(self):
        """test buffer number is returned after """
        x = "100"
        self.assertTrue(x==str(DigitalBufferUnit(3,ptype=Unary.P1)))
    
    def test2(self):
        """test buffer number is returned after """
        x = "1000"
        self.assertTrue(x==str(DigitalBufferUnit(3,ptype=Unary.P10)))

    def test3(self):
        """test buffer number is returned after """
        x = "101"
        self.assertTrue(x==str(DigitalBufferUnit(3,ptype=Unary.P2)))

    def test4(self):
        """test buffer number is returned after """
        x = "10001"
        self.assertTrue(x==str(DigitalBufferUnit(3,ptype=Unary.P20)))

    def test41(self):
        """test buffer number is returned after """
        x = "101"
        self.assertTrue(x==str(DigitalBufferUnit(1,ptype=Unary.P20)))

    def test5(self):
        """test dirty buffer number is returned after """
        x = [1,0,0,1,0,0]
        x_ = "".join([str(i) for i in x ])
        self.assertTrue(x_==str(DirtyDigitalBufferUnit(x)))

    def test6(self):
        """test dirty buffer number is returned after """
        x = [0,1,0,0,1,0]
        x_ = "".join([str(i) for i in x ])
        self.assertTrue(x_==str(DirtyDigitalBufferUnit(x)))
            #
    def test7(self):
        t = DigitalBufferUnit(3,ptype=Unary.P20)
        p = ViewerUnit()
        t.connect(lambda: p.ports["in"])
        temp = []
        for _ in range(5):
            t.tick()
            temp +=[p.tick()]
        self.assertTrue(t.clock==5)

    def test8(self):
        t = DigitalBufferUnit(3,ptype=Unary.P20)
        p = ViewerUnit()
        t.connect(lambda: p.ports["in"])
        temp = []
        for _ in range(5):
            t.tick()
            temp +=[p.tick()]
        self.assertTrue(temp==[1,0,0,0,1])

    def test9(self):
        x = [0,1,0,0,1,0]
        t = DirtyDigitalBufferUnit(x)
        p = ViewerUnit()
        t.connect(lambda: p.ports["in"])
        temp = []
        for _ in range(6):
            t.tick()
            temp +=[p.tick()]
        self.assertTrue(temp==[0,1,0,0,1,0])

    def test10(self):
        a = DigitalBufferUnit(3,ptype=Unary.P20)
        b = DigitalBufferUnit(3,ptype=Unary.P20)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(5):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[1,0,0,0,1] and temp2==[1,0,0,0,1])

    def test101(self):
        a = DigitalBufferUnit(1,ptype=Unary.P20)
        b = DigitalBufferUnit(1,ptype=Unary.P20)
        a.new(3,ptype=Unary.P20)
        b.new(4,ptype=Unary.P20)
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        b.connect(lambda: _b.ports["in"])
        
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        print(temp1)
        print(temp2)
        self.assertTrue(temp1==[1,0,0,0,1,0] and temp2==[1,0,0,0,0,1])    

    def test102(self):
        a = DigitalBufferUnit(1,ptype=Unary.P20)
        b = DigitalBufferUnit(1,ptype=Unary.P20)
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        b.connect(lambda: _b.ports["in"])
        a.new(3,ptype=Unary.P20)
        b.new(4,ptype=Unary.P20)
        
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        print(temp1)
        print(temp2)
        self.assertTrue(temp1==[1,0,0,0,1,0] and temp2==[1,0,0,0,0,1])    

    def test11(self):
        x = [0,1,0,0,1,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,1,0,0,1,0] and temp2==[0,1,0,0,1,0] )

    def test12(self):
        x = [0,1,0,0,1,0]
        y = [1,0,0,1,0,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(y)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,1,0,0,1,0] and temp2==[0,1,0,0,1,0] )

    def test13(self):
        x = [0,1,0,0,1,0]
        y = [1,0,0,1,0,0]
        a = DirtyDigitalBufferUnit(y)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,1,0,0,1,0] and temp2==[0,1,0,0,1,0] )


    def test14(self):
        x = [0,0,1,0,0,1,0]
        y = [1,0,0,1,0,0,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(y)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(7):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,1,0,0,1,0] and temp2==[0,0,1,0,0,1,0] )

    def test15(self):
        x = [0,0,1,0,0,1,0]
        y = [1,0,0,1,0,0,0]
        a = DirtyDigitalBufferUnit(y)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(7):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,1,0,0,1,0] and temp2==[0,0,1,0,0,1,0] )
                                #
    def test16(self):
        a = DigitalBufferUnit(3,ptype=Unary.P20)
        b = DigitalBufferUnit(4,ptype=Unary.P20)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(6):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[1,0,0,0,1,0] and temp2==[1,0,0,0,0,1] )
            
    def test17(self):
        x = [0,0,0,1,0,0,1,0]
        y = [1,0,0,1,0,0,0,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(y)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(8):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,1,0,0,1,0] and temp2==[0,0,0,1,0,0,1,0] )

    def test18(self):
        x = [0,0,0,1,0,0,1,0]
        y = [1,0,0,1,0,0,0,0]
        a = DirtyDigitalBufferUnit(y)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(8):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,1,0,0,1,0] and temp2==[0,0,0,1,0,0,1,0] )

    def test19(self):
        x = [0,0,0,0,1,0,0,1]
        y = [1,0,0,1,0,0,0,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(y)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(8):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,0,1,0,0,1] and temp2==[0,0,0,0,1,0,0,1] )

    def test20(self):
        x = [0,0,0,0,1,0,0,1]
        y = [1,0,0,1,0,0,0,0]
        a = DirtyDigitalBufferUnit(y)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(8):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,0,1,0,0,1] and temp2==[0,0,0,0,1,0,0,1] )

    def test21(self):
        x = [0,0,0,0,0,1,0,0,1]
        y = [1,0,0,1,0,0,0,0,0]
        a = DirtyDigitalBufferUnit(x)
        b = DirtyDigitalBufferUnit(y)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(9):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,0,0,1,0,0,1] and temp2==[0,0,0,0,0,1,0,0,1] )

    def test22(self):
        x = [0,0,0,0,0,1,0,0,1]
        y = [1,0,0,1,0,0,0,0,0]
        a = DirtyDigitalBufferUnit(y)
        b = DirtyDigitalBufferUnit(x)
        p = SyncUnit()
        _a = ViewerUnit()
        _b = ViewerUnit()
        a.connect(lambda: p.ports["in1"])
        b.connect(lambda: p.ports["in2"])
        p.connect("out1", lambda: _a.ports["in"])
        p.connect("out2", lambda: _b.ports["in"])
        temp1,temp2 = [],[]
        for _ in range(9):
            a.tick()
            b.tick()
            p.tick()
            temp1 +=[_a.tick()]
            temp2 +=[_b.tick()]
        self.assertTrue(temp1==[0,0,0,0,0,1,0,0,1] and temp2==[0,0,0,0,0,1,0,0,1] )

    def test23(self):
        a = RecurringDigitalBufferUnit(3,ptype=Unary.P20)
        _a = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        out = []
        for _ in range(13):
            a.tick()
            out +=[_a.tick()]
        self.assertTrue(out==[1,0,0,0,1,0,0,0,1,0,0,0,1] )


    def test231(self):
        a = RecurringDigitalBufferUnit(7,ptype=Unary.P20)
        _a = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        out = []
        for _ in range(17):
            a.tick()
            out +=[_a.tick()]
        self.assertTrue(out==[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1] )

    def test232(self):
        a = RecurringDigitalBufferUnit(3,ptype=Unary.P1)
        _a = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        out = []
        for _ in range(13):
            a.tick()
            out +=[_a.tick()]
        self.assertTrue(out==[1,0,0,1,0,0,1,0,0,1,0,0,1] )

    def test24(self):
        a = RecurringDigitalBufferUnit(1,ptype=Unary.P20)
        _a = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        out = []
        for _ in range(13):
            a.tick()
            out +=[_a.tick()]
        self.assertTrue(out==[1,0,1,0,1,0,1,0,1,0,1,0,1] )

    def test25(self):
        a = DigitalBufferUnit(3,ptype=Unary.P20)
        b = DigitalBufferUnit(5,ptype=Unary.P20)

        c = MinMaxCoincUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(7):
            a.tick()
            b.tick()
            c.tick()
 
        self.assertTrue(c.ports["max"][1]==5 and c.ports["min"][1]==3)

    def test26(self):
        a = DigitalBufferUnit(7,ptype=Unary.P20)
        b = DigitalBufferUnit(5,ptype=Unary.P20)

        c = MinMaxCoincUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(9):
            a.tick()
            b.tick()
            c.tick()
            
        self.assertTrue(c.ports["max"][1]==7 and c.ports["min"][1]==5)

    def test27(self):
        a = DigitalBufferUnit(7,ptype=Unary.P20)
        b = DigitalBufferUnit(5,ptype=Unary.P20)

        c = MinMaxCoincUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(9):
            a.tick()
            b.tick()
            c.tick()
        self.assertTrue(c.ports["max"][1]==7 and c.ports["min"][1]==5)

    def test28(self):
        a = DigitalBufferUnit(7,ptype=Unary.P20)
        b = RecurringDigitalBufferUnit(5,ptype=Unary.P1)

        c = ModUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(9):
            a.tick()
            b.tick()
            c.tick()

          
        self.assertTrue(c.ports["div"][1]==1 and c.ports["rem"][1]==2)

    def test28(self):
        a = DigitalBufferUnit(7,ptype=Unary.P20)
        b = RecurringDigitalBufferUnit(3,ptype=Unary.P1)

        c = ModUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(9):
            a.tick()
            b.tick()
            c.tick()
          
        self.assertTrue(c.ports["div"][1]==2 and c.ports["rem"][1]==1)

    def test29(self):
            a = DigitalBufferUnit(11,ptype=Unary.P20)
            b = RecurringDigitalBufferUnit(3,ptype=Unary.P1)
    
            c = ModUnit()
            a.connect(lambda: c.ports["in1"])
            b.connect(lambda: c.ports["in2"])
            
            out = []
            for _ in range(13):
                a.tick()
                b.tick()
                c.tick()
              
            self.assertTrue(c.ports["div"][1]==3 and c.ports["rem"][1]==2)

    def test30(self):
        a = ClockedDigitalBufferUnit(10,2,ptype=Unary.P2)
        _a = ViewerUnit()
        a.connect(lambda: _a.ports["in"])
        out = []
        out1 = []
        for _ in range(10):
            a.tick()
            o = _a.tick()
            out +=[o[0]]
            out1 +=[o[1]]
    
        self.assertTrue(out==[1,0,0,0,0,0,0,0,0,1] and out1==[1,0,1,0,1,0,1,0,1,0] )

    def test31(self):
        a = ClockedDigitalBufferUnit(10,2,ptype=Unary.P2)
        b = ClockedDigitalBufferUnit(6,2,ptype=Unary.P2)

        c = ClockedMinMaxCoincUnit()
        a.connect(lambda: c.ports["in1"])
        b.connect(lambda: c.ports["in2"])
        
        out = []
        for _ in range(10):
            a.tick()
            b.tick()
            c.tick()
        self.assertTrue(c.ports["max"][1]==5 and c.ports["min"][1]==3)

    def test32(self):
        a = ClockedDigitalBufferUnit(10,2,ptype=Unary.P2)
        
        c = ClockedDivideUnit()
        a.connect(lambda: c.ports["in1"])
        
        out = []
        for _ in range(10):
            a.tick()
            c.tick()
        self.assertTrue(c.ports["div"][1]==5 and c.ports["rem"][1]==0)

    def test33(self):
        w1 = WhileUnit(to_temporal(0, ptype=Unary.P20))
        a = DigitalBufferUnit(33,ptype=Unary.P20)
        a.connect(lambda: w1.ports["test"])
        w1.tick()
        self.assertTrue(w1.ports["out"][1]=="cont")

    def test34(self):
        w1 = WhileUnit(to_temporal(0, ptype=Unary.P20))
        a = DigitalBufferUnit(0,ptype=Unary.P20)
        a.connect(lambda: w1.ports["test"])
        w1.tick()
        self.assertTrue(w1.ports["out"][1]=="cont")
        
        
    def testGCD(self):
        
        w1 = WhileUnit(to_temporal(0, ptype=Unary.P2))
        a = DigitalBufferUnit(45,ptype=Unary.P20)
        b = RecurringDigitalBufferUnit(15,ptype=Unary.P1)
        # Setup the ports

        m1 = ModUnit()
        a.connect(lambda: m1.ports["in1"])
        b.connect(lambda: m1.ports["in2"])

        m1.connect("rem", lambda: w1.ports["test"])
        

        #run the operation/update loop
        main_status = False
        c = 0
        while not main_status:
            status = False
            # c+=1
            while not status:
                a.tick()
                b.tick()
                # print(m1.ports["in1"])
                # print(m1.ports["in2"])
                status = m1.tick()
                # print(status)
            w1.tick()
            rem = m1.ports["rem"][1]
            clock =  m1.ports["clock"][1]
            main_status = rem==0
            print(main_status)
            m1.reset()
            print(rem)
            print(clock)
            a.new(clock,Unary.P20)
            b.new(rem,Unary.P1)
            # print(a.ports["buffer"])
            # print(b.ports["buffer"])


            # for i in range(17):
                # a.tick()
                # b.tick()
                # print(m1.ports["in1"])
                # print(m1.ports["in2"])
                # status = m1.tick()
                # print(status)
            
        self.assertTrue(clock==15)
    
if __name__ == '__main__':
    unittest.main()



