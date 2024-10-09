from temporalunit import *

def main():
    """main"""
    print("Starting")
    m1 = ModUnit()
    w1 = WhileUnit()

    # Setup the ports
    m1.connect("mod", lambda: m1.ports["val"], True)
    m1.connect("val", lambda: w1.ports["test"])
    w1.connect("test", lambda: m1.ports["mod"])

    #set some initial values
    m1.ports["val"][1] = 33
    m1.ports["mod"][1] = 15
    print(m1)
    print(w1)

    #run the operation/update loop
    while True:
        m1.op()
        print(m1)
        m1.update()
        w1.op()
        print(w1)
        w1.update()
        
 
if __name__ == "__main__":
    main()    
