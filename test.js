class A{

    test(){
        console.log("run A");
        this.test2();
    }

}


class B extends A{
    test2(){
        console.log("run B")
    }
}



let b = new B();

B.test()