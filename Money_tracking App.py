import sys
class Record:
    def __init__(self, category, item, amount ):
        """
        Initialize a record that holds "category", "item", "amount" fields.
        Arguments:
            category: which category the item belongs to.
            item: the expense or income activity
            amount: the amount of money spent of earned
        """
        self._category = category
        self._item = item
        self._amount = int(amount)
    @property
    def _get_category(self):
        """
        It gets the attribute: "category" of the instance.
        """
        return self._category
    @property
    def _get_item(self):
        """
        It gets the attribute: "item" of the instance.
        """
        return self._item
    @property
    def _get_amount(self):
        """
        It gets the attribute: "amount" of the instance.
        """
        return int(self._amount)
    def __repr__(self):
        """
        It prints out the class and initial parameter in the constructor.
        """
        return f'Record({self._category}, {self._item}, {self._amount})'


class Record_list():
    def __init__(self):
        """
        Constructor. 
        It initialize a record list object which is essentially a list of class Record's object.       
        """
        self._record_list = list()
        try:
            with open('records.txt') as rt:
                
                if len(rt.readlines())== 0: #8
                    raise FileNotFoundError
                
                rt.seek(0)
                try: #9
                    self._init_money = int(rt.readline().strip('\n'))
                except ValueError:
                    sys.stderr.write('Invalid initial amount of money\n')
                    self._init_money = int(input('Please input integer initial money:'))
                
                record_content = rt.readlines()[:] #list of strings(each string:'cat item amount'), reading from 2nd element, rt header moves to 2nd element
                temp_list = list(map(lambda r: r.strip('\n').split(), record_content)) #temp_list: [[ cat ,item , amount ], [ cat , item , amount]]

                for i in temp_list:
                    try: #10-1
                        if len(i) != 3: #10 when record cannot be splitted to 2 string
                            raise ValueError
                    except ValueError: #10. second string cannot turn into integer OR not split into 2 string
                        sys.stderr.write('\nInvalid format in records.txt. Deleting the contents.') 
                        continue # 3 lines before, append any, if there's issue, pop it.
                    
                    try: #10-2
                        i[-1] = int(i[-1])
                    except ValueError:
                        sys.stderr.write('\nPrice cannot be character. Deleting invalid record.')
                        continue # goes to next item in 'record_content'
                       
                    self._record_list.append(Record(i[0], i[1], i[-1]))
        
        except FileNotFoundError: #7
            try:
                self._init_money = int(input('There is no record for now, input your initial amount of money:'))

            except ValueError as err1: #1 exception
                sys.stderr.write(str(err1) + '\n')
                self._init_money = int(input('Please input integer:'))


    
    def add(self, record, categories_obj):
        """
        Add item whose category field is in the categories passed in to the record list.
        Arguments:
            record: the input from the user
            categories_obj: a class "Categories" object
        """
        rxp_string_list = record.split(sep = ',') #rxp: record and expense
        for i in rxp_string_list:
            temp_list = i.split() #split by space into: i =  ['c1' 'i1' 'a1'], temp_list = ['c1', 'i1', 'a1']

            if len(temp_list) != 3: #3
                sys.stderr.write('The format of a record should be like this: meal breakfast -50.\nFail to add a record.')
                break #break for, if cannot split into 2 string, don't add the item
            try: #4
                temp_list[-1] = int(temp_list[-1]) #turn 'e1' into integer e1
            except ValueError:
                sys.stderr.write('Invalid value for money.\nFail to add a record.')
                break
            try:
                if Categories.out_is_category_valid(  temp_list[0] , categories_obj._categories):
                    self._record_list.append(Record(temp_list[0], temp_list[1], temp_list[-1]))  # item_expense_pair is tuple, mutable
                else:
#                     print(f'list passed in is {categories_obj.categories}')
                    raise ValueError
            except ValueError:
                sys.stderr.write('Invalid category name.')
        
    def view(self):
        """
        View everything in the record list and calculate their balance.
        """
        #formating is important
        #category name
        print('{0: <21s}{1: <21s}{2:<6s}'.format('Category','Desciption','Amount'))
        #division mark
        
        print('{0: <21s}{1: <21s}{2:<6s}'.format('====================','====================','======'))
        #print list: 21 padding, 6 padding, all left align
        
        for i in self._record_list: # i is the object(instance)
            print('{0: <21s}{1: <21s}{2:<6d}'.format(i._get_category, i._get_item, i._get_amount))
        #division mark
        print('{0: <21s}{1: <21s}{2:<6s}'.format('====================','====================','======'))

        #Calculate balance
        balance = sum( i._get_amount for i in self._record_list) + self._init_money
        #Now you have --- dollars.
        print('Now you have {:d} dollars.'.format(balance))

       
    def delete(self):
        """
        Display the record list table with index for user to delete items.
        """
        

    #display
       #category name
        print('{: <6s}{: <21s}{: <21s}{:<6s}'.format('Index','Category','Desciption','Amount'))

        #division mark
        print('{: <6s}{: <21s}{: <21s}{:<6s}'.format('=====','====================','====================','======'))

        #print list: 21 padding, 6 padding, all left align (enumeration)
        for i, v in enumerate(self._record_list): 
            print('{: <6d}{: <21s}{: <21s}{:<6d}'.format(i,v._get_category,v._get_item, v._get_amount))

        #division mark
        print('{: <6s}{: <21s}{: <21s}{:<6s}'.format('=====','====================','====================','======'))

        #prompt, delete using index as reference
        try:#5,6
            index = int(input('Please specify the index of the item you want to delete:'))

            #delete
            del(self._record_list[index]) # del is mutable, default list is changed, rxp_tuple_list is actually changed("call by object reference")

        #     """    
        #     Python utilizes a system, which is known as “Call by Object Reference” or “Call by assignment”. 
        #     In the event that you pass arguments like whole numbers, strings or tuples to a function, the passing is 
        #     like call-by-value because you can not change the value of the immutable objects being passed to the function.
        #     Whereas passing mutable objects can be considered as call by reference because when their values are change
        #     d inside the function, then it will also be reflected outside the function.
        #     """
        #delete
        except ValueError:#5
            sys.stderr.write('\nInvalid Index. Fail to delete a record.')
        except IndexError:#6
            sys.stderr.write('\nIndex out of Bound, Try again. Fail to delete.')


    def save(self):
        """
        Save the record in the record list to my_records.txt.
        """
        with open('records.txt','w') as rt:   
        # write init_money into records.txt
            rt.write(str(self._init_money) + '\n')
            rt.writelines(list(map(lambda r: str(r._get_category) + ' ' + str(r._get_item) + ' ' + str(r._get_amount) + '\n', self._record_list)))
        #pass lst's element as argument:x for lambda anonymous function, map() apply function on each iterable elements(now tuple)
        # write records into records.txt
          
    def find(self, L):
        """
        Show all records whose category belongs to the passed in list L. 
        Then report the total amount of money of the listed records.
        """
        #formating is important
        #category name
        print('{0: <21s}{1: <21s}{2:<6s}'.format('Category','Desciption','Amount'))
        #division mark
        
        print('{0: <21s}{1: <21s}{2:<6s}'.format('====================','====================','======'))
        #print list: 21 padding, 6 padding, all left align
        
        for i in self._record_list: # i is the object(instance)
            if i._get_category in L:
                print('{0: <21s}{1: <21s}{2:<6d}'.format(i._get_category, i._get_item, i._get_amount))
        #division mark
        print('{0: <21s}{1: <21s}{2:<6s}'.format('====================','====================','======'))

        #Calculate balance
        balance = sum( i._get_amount for i in self._record_list if i._get_category in L) #+ self._init_money
        #Now you have --- dollars.
        print('Total amount of money in listed record is {:d} dollars.'.format(balance))
                
                

                
                
                
# a = Record_list()
# print(a.init_money)
# for i in a.record_list:
#     print(i)

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """
        Initialize a nested list that contains hiearchical categories as the attribute: "categories" of the object.
        """
    # 1. Initialize self.__categories as a nested list.
        predefined_mult_list = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonu\
s']]
        self._categories = predefined_mult_list
    
    #categories.indent()
    def view(self):
        """
        View categories with indentation to show hiearchical structure.
        """
        #categories.indent()
        def indent_list(L, level=0):
            if L == None:
                return
            if type(L) in {list, tuple}:
                for child in L:
                    indent_list(child, level+1)
            else:
                print(f'{" "*4*(level-1)}' + f'-' + f"{L}")
        
        indent_list(self._categories)
      
        #flatten and is_category_valid
#     @staticmethod
#     def _flatten(categories): #categores: predefined one, pass in by add( ,categories)
#         def flatten(categories):
#             ls = list() #initialize
#             if categories is None: # base case
#                 return  # raises StopIteration
#             if type(categories) in {list, tuple}: # recursive
#                 for child in categories: # recursively generate each child of L
#                     ls.extend( flatten(categories= child))# anything yielded must be atom 
#                 return ls
#             else: # base case
#                 return [categories]
#         return flatten(categories)
    @staticmethod
    def out_is_category_valid(category, categories_mult_list):
        """
        Shows true if  category is in "categories_mult_list", else False.
        Return whatever is returned from the inner function after calling it.
        """
        def is_category_valid(category, categories_mult_list):
            """
            A recursive function that checks if category is in "categories_mult_list.
            Return: boolean value.
            """
            if type(categories_mult_list) in {list, tuple}:
#                 print(f'{categories_mult_list} is a list, searching through it')
                for child in categories_mult_list:
#                     print(f'Now search {child}')
                    p = is_category_valid(category, child )
                    if p == True:
                        return True
                    else:
                        continue
            else:
#                 print(f'is an atom, compare {categories_mult_list} =? {category} ')
                return category == categories_mult_list 
        return is_category_valid(category, categories_mult_list)
    

    def find_subcategories(self, category):
        """
        Use inner generator to return a flattened list of target category and it's subcategories.
        """
        categories = self._categories
        def find_subcategories_gen(category, categories, found=False):
            """
            A recursive generator to return a flattened list of target category and it's subcategories.
            Arguments:
                category: target category, of type string.
                categories: the predefined multlist to search from.
                found: a flag to enable detection of subcategories after target category is found.
                
            """
            if type(categories) == list:
#                 print(f'\n{categories} is list, search through it')

                for index, child in enumerate(categories):

#                     print(f'(1) Now search  child:: {child}, found ={found}')
                    yield from find_subcategories_gen(category, child, found )

                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list: 
#                         print(f'(2) {child} == {category}, Category found, \
#                         next is sub_list. Search through subcategories: {categories[index +1]}, found = {found}')
                        yield from ( find_subcategories_gen( category, categories[ index + 1], True ))

            else:

#                 print(f'(3-1)    {categories} is atom')

                if categories == category or ( found == True ):

#                     print(f'(3-2) compare {category} =? {categories}, found = {found}')
                    yield categories
        return [x for x in find_subcategories_gen(category, self._categories)]

# a = Categories()
# a.view()
# a.find_subcategories('bus')


# class definitions here
categories = Categories()
record_list = Record_list()
while True:
    command = input('\nWhat do you want to do (add / view/ delete/ view categories/ find/ exit)? ')
    if command == 'add':
        record = input('Add an expense or income record with format: categories item amount. Ex. meal mcDonald -120\n')
        record_list.add(record, categories)
    elif command == 'view':
        record_list.view()
    elif command == 'delete':
        record_list.delete()
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        record_list.find(target_categories)
    elif command == 'exit':
        record_list.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
