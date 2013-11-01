    def predict_rating(self, movie):
        ratings = self.ratings # ratings object for the user that we want prediction for
        other_ratings = movie.movie_ratings # all rating objects for the movie object
        
        similarities = [(self.similarity(r.user), r) for r in other_ratings] 
        # list of tuples of [(similarity, rating object)]
        
        similarities.sort(reverse=True) # sorted list starting with [(highest sim, rating object)]

        top_user = similarities[1] # tuple of sim, rating object

        return top_user[1].rating * top_user[0] # rating * similarity