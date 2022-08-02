class Cart():
        #add new item in Cart
        def additem(self,newitemrow,cart_lst):
            cart_lst.append(newitemrow)
            return cart_lst

        #remove last item from cart same as undo
        def cart_undo(self,cart_lst,index=-1):
            if(cart_lst is not None):
                if(index==-1):
                    cart_lst.pop()
                else:
                    cart_lst.pop(index)
            return cart_lst

        #remove all item from cart
        def cart_clear(self,cart_lst):
            cart_lst.clear()
            return cart_lst

        #edit cart Qntity
        def cart_edit(self,xid, newqnty, cart_list):
            for row in  cart_list:
                if(row[0]==(xid-1)):
                    row[2]=newqnty
            return cart_list

        #count total item purchases in cart
        def count_item(self,cart_list):
            x=len(cart_list)
            return x

        #total amount of all product in cart
        def cart_amount(self,cart_lst):
            sum=0
            for row in cart_lst:
                total=row[5]*1
                sum+=total
            return sum


        def cart_del(self, id,cart_lst):
            newcart=list()
            count=0
            for row in cart_lst:
                if(str(id) != str(row[1])):
                    newcart.append(row)
                    count=self.count_item(newcart)
            return newcart , count
                


    
