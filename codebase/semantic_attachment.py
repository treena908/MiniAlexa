import nltk
from nltk.sem.logic import Expression, LambdaExpression
from nltk import grammar, parse
import logging


class SemUtil:

    def __init__(self):
        pass

    @staticmethod
    def quote(str):
        return '\'' + str + '\''

    @staticmethod
    def clearNonterminal(N):
        if len(N.symbol().split('+')) > 1:
            return ''.join(N.symbol().split('+'))
        else:
            return N.symbol()


class SemanticAttachment:

    def __init__(self):
        pass
    
  
    def treeCallback(self, tree, height):
        prod = tree.productions()[0]
        lhs = prod.lhs().symbol()
        #print("lhs %s %d" %(lhs,tree.height() ) )
        if tree.height() == 2:

            rhs = prod.rhs()[0]
            
            if lhs in ['.', '?', ':']:
                return ''

            if len(lhs.split('+')) > 1:
                lhs = ''.join(lhs.split('+'))

            if lhs in ['VB', 'VBN', 'VBZ', 'VBD'] and (not rhs[0].isupper()):
                sem = lhs + '[SEM=(<\\x \\y.' + rhs + '(y,x)>)] -> ' + SemUtil.quote(rhs)
            elif (lhs in ['DT', 'IN', 'JJS']) and (rhs not in ['highest', 'higher', 'deepest', 'deeper']):
                sem = lhs + '[SEM=()]' + '->' + SemUtil.quote(rhs)
            else:
                sem = lhs + '[SEM=(' + SemUtil.quote(rhs) + ')]' + ' -> ' + SemUtil.quote(rhs)

        else:
            rhs = prod.rhs()
            
            #rhs = map(SemUtil.clearNonterminal, rhs)
            rhs = list(map(SemUtil.clearNonterminal, rhs))
            #print("rhs %d" %(len(list(rhs))) )
            #print("rhs %s" %(rhs) )
            if tree.height() == height:
                
                lhs = 'SS'
            
            if len(lhs.split('+')) > 1:
                
                lhs = ''.join(lhs.split('+'))

            cnt = 0
            sem = lhs + '[SEM=(' + ' + '.join(['?' + rhs[i].lower() + str(i) for i in range(len(rhs))]) + ')]' + ' -> ' + ' '.join(
                [rhs[i] + '[SEM=?' + rhs[i].lower() + str(i) + ']' for i in range(len(rhs))])
            
        return sem + '\n'

    def traverseTree(self, tree, height):
        semgram = self.treeCallback(tree, height)
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                subsemgram = self.traverseTree(subtree, height)
                if subsemgram is not None:
                    semgram = semgram + subsemgram
        return semgram
    def check(self,myStr): 
        stack = [] 
        open_list = ["("] 
        close_list = [")"] 
        if myStr is not None:
            
            for i in myStr:
                
                if i in open_list: 
                    stack.append(i) 
                elif i in close_list: 
                    pos = close_list.index(i) 
                    if ((len(stack) > 0) and
                        (open_list[pos] == stack[len(stack)-1])): 
                        stack.pop()
                    
                    else: 
                        return "Unbalanced",stack
                
            if len(stack) == 0: 
                return "Balanced",stack
            else: 
                return "Unbalanced",stack
    def lambdaReducer(self, tree):
        read_expr = Expression.fromstring # logical expression reader
        answer = tree[0].label()['SEM'] # generated string would be at the root of the tree
        #print(answer)
        final_list=[]
        ans=str(answer)[2 : -2 ] 
        answer1=ans.split(', ')
        
        #print(answer)
        
        lst_arguments = []
        lst_funcs = []
        #print(ans.split(',')[0])
        for item in answer1:
            item=str(item)
            #print(item)
            if len(item.split('.'))>1:
                
                item=item[item.find('\\'):item.find(')')+1]
                final_list.append(item)
            else:
                if item is not None:
                    checks,stack=self.check(item)
                    
                    if checks=="Unbalanced":
                        
                        if len(stack)>0:
                            
                            while len(stack)>0:
                                #print(stack)
                                item=item[1: :]
                                stack.pop()
                        else:
                            
                            item=item[:-1 :]
                final_list.append(item)  
        
        for item in final_list:   
            if isinstance(item, LambdaExpression):
                #print(item)
                lst_funcs.append(item)
            else:
                #print('else')
                
                #print(item)
                if isinstance(item, nltk.featstruct.FeatureValueTuple):
                    if item.__repr__() in ['(which)', '(who)', '(where)', '(when)']:
                        lst_arguments.append('(wh)')
                    elif len(item.__repr__().split('.')) > 1: 
                        lst_funcs.append(item.__repr__()[1:-1])
                    else:
                        lst_arguments.append(item.__repr__()) 
                elif len(item.__repr__().split('.')) > 1: # lambda expression
                        lst_funcs.append(item.__repr__()[2:-1])
                elif item in ['which', 'who', 'where', 'when']:
                    #print('hi')
                    lst_arguments.append('(wh)')
                elif item not in ['oscar']:
                    lst_arguments.append('('+item+')')

        if len(lst_funcs) > 1:
            lst_funcs = [func for func in lst_funcs if str(func).split('.')[1].split('(')[0] not in ['is', 'was', 'did', 'has']]
        #print(lst_funcs)
        #print(lst_arguments)
        fs = ""
        fs += str(lst_funcs[0])
        #print(fs)
        for item in lst_arguments:
            fs += item
        #print(fs)
        #fs='\\x y.is(y,x)((Kubrick))(director)'
        fexp = read_expr(fs)
        return fexp.simplify()

    def getSemanticFromParseTree(self, question, parse_tree):
        #try:
        semgram = '% start SS\n' + self.traverseTree(parse_tree, parse_tree.height())
        logging.debug('Semantic Grammar: %s', semgram)

        semgrammar = grammar.FeatureGrammar.fromstring(semgram)
        semparser = parse.FeatureEarleyChartParser(semgrammar)
        tree = list(semparser.parse(question.split()))
           
        return self.lambdaReducer(tree)
        #except Exception as exp:
            #logging.error('Domain: %s', exp)

