from sqlite_db_manager import SqliteManager
from  nltk.parse.corenlp  import CoreNLPParser
import question_classification
from semantic_attachment import SemanticAttachment
from semantic_sql_query import SQL_Semantic



parser = CoreNLPParser(url='http://localhost:9000')
db_manager = None
question_classification.initialize()
databases = {
    'movie' :   'Sqlite.Db/oscar-movie_imdb.sqlite',
    'music' :   'Sqlite.Db/music.sqlite',
    'geography' :   'Sqlite.Db/WorldGeography.sqlite'
}

questions = [
    'Is Kubrick a director?',
    'Is Neeson an actor?',
    'Is Mighty Aphrodite by Allen?',
    'Was Loren born in Italy?',
    'Was Birdman the best movie in 2015?',
    'Did Neeson star in Schindler\'s List?',
    'Did Swank win the oscar in 2000?',
    'Did a French actor win the oscar in 2012?',
    'Did a movie with Neeson win the oscar for best film?',
    'Who directed SchindlersList?',
    'Who won the oscar for best actor in 2005?',
    'Who directed the best movie in 2010?',
    'Which actress won the oscar in 2012?',
    'Which movie won the oscar in 2000?',
    'When did Blanchett win an oscar for best actress?',
    'Did Jamie Foxx win the oscar for best actor in 2005?',
    'Which French actor win the oscar in 2012?',
    #'Which movie with Neeson win the oscar for best film?',
    'Did MerylStreep won the oscar in 2012?',
    'When did Meryl Streep won the oscar for best actress?',
    'Where did Loren born?',
    'Did Spielberg direct Schindler\'s List?',
    'Did Madonna sing Papa Do Not Preach?',
    'Does the album Thriller include the track Beat It?',
    'Which album by Beyonce was released in 2014?',
    
    'Which is the highest mountain in the world?',
    'Where is the highest mountain?',
    'Which is the deepest ocean?',
    'Is K2 taller than Makalu?',
    'Which continent has the highest population?',
    'What is the genre of the album Thriller?',
    'Which artist released the album 1989?',
    'Which pop singer was born in Miami in 1958?'
]








def preprocess_question(q):
        q = q[:-1]
        q = q.split(' ')[0].lower() + ' ' + ' '.join(q.split(' ')[1:])
        sq = q.split(' ')
        sq = [w.split('\'')[0] for w in sq]
        sq = [w.split(':')[0] for w in sq]
        sq = ['*'.join(w.split('-')) for w in sq]
        return ' '.join(sq)
def answer(q):

   
    
    try:
        domain = question_classification.load_question(q)
        db_manager = SqliteManager(databases[domain])
      

    except Exception as error:
        print 'Classification error'

    
    
   
    q = preprocess_question(q)
  
    tree = next(parser.raw_parse(q))
   
    sem_analyser = SemanticAttachment()
    semantic = sem_analyser.getSemanticFromParseTree(q, tree)
    #print '<SEMANTIC>: ', semantic

    if semantic is  None:
        
        return 'I don\'t know'
    else:

        try:
            sql_semantic = SQL_Semantic(semantic, domain)
            sql_queries = sql_semantic.build_sql_from_semantic()
            
            print '<Query>: \n', sql_queries

            if len(sql_queries) == 0:
                return 'I don\'t know'
            else:
                answer = db_manager.processQueries(sql_queries)
                return  answer
        except Exception as error:
           
            return 'I don\'t know'


def main():

     

    
    for q in questions:
        #Sq=q.strip('\n')
        
        print "<QUESTION>: ", q
    
        a = answer(q)
        
        print '<ANSWER>: ', a
        print ('')
        


if __name__ == "__main__":
    main()



























