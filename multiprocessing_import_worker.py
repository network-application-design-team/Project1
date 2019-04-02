import pickle 

def worker(n):
    """worker function"""
    prime(n)
    return

def prime(n):
    n = pickle.loads(n)
    n = n[1]
    list = []
    for num in range(1,n):
        if all(num%i!=0 for i in range (2,num)):
            list.append(num)
        print(max(list))
        return max(list)
