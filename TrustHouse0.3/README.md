# Trust House v. 0.3 #

In this version I will include map the postcodes to a map I will create using `Folium`.

For this to work the way I intend, I will create another table for the logitude & latitude - and give it a *one to one* relationship between the `Address` table and the `Map` table.

For now, every new postcode is stored in the `Map` table with their latitude & longitude co-ordinates, in order to user the same cordinates to plot on a generated map.

Later, I will update each address plot with the number of reviews each postcode has - this might require some refactoring of my database models.

For my next step I will need to calculate the length of the reviews and then add it to the associated address.
The `Address` table will have an additional column - `total_reviews`.

Will have to get the data through the `Review` table via the foriegn key

```
revs = Review.query.all()

for r in revs:
    count = 0
    if r.address.postcode == 'sw17 0en':
        count += 1
        # update the number of reviews in Adress table for matching postcode
        # if review.address_id is == to address.id then we update the number of reviews with count variable
        #
```
looks like I will need to refactor db models in v.0.4:
- remove the map table
- include longitude & latitude cordinates in `Address` table
- add extra column -->`total_reviews` or `review_count` to `Address` table