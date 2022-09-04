# Trust House v. 0.3 #

In this version I will include map the postcodes to a map I will create using `Folium`.

For this to work the way I intend, I will create another table for the logitude & latitude - and give it a *one to one* relationship between the `Address` table and the `Map` table.

For now, every new postcode is stored in the `Map` table with their latitude & longitude co-ordinates, in order to user the same cordinates to plot on a generated map.

Later, I will update each address plot with the number of reviews each postcode has - this might require some refactoring of my database models.