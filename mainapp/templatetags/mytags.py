from django import template
register = template.Library()

@register.filter(name='paymentMode')
def paymentMode(Request,num):
    if(num==0):
        return 'COD'
    else:
        return "Net Banking"
    
@register.filter(name='paymentStatus')
def paymentStatus(Request,num):
    if(num==0):
        return 'Pending'
    else:
        return "Done"
    
@register.filter(name='orderStatus')
def orderStatus(Request,num):
    if(num==0):
        return 'Order Placed'
    elif(num==1):
        return 'Ready to Pack'
    elif(num==2):
        return 'Packed'
    elif(num==3):
        return 'Ready to Ship'
    elif(num==4):
        return 'Shipped'
    elif(num==5):
        return 'Order in Transit'
    elif(num==6):
        return 'Product reached at final destination'
    elif(num==7):
        return 'Out for Delievery'
    else:
        return "Delievered"