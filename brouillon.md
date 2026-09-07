 url d'accueil : https://books.toscrape.com/index.html

 url d'un livre : https://books.toscrape.com/catalogue/olio_984/index.html

 **construction d'une url :**
 -> https://books.toscrape.com/
 -> catalogue/
 -> nomdulivre_numerodulivre
 -> /index.html

 catalogue :
 https://books.toscrape.com/catalogue/category/books_1/index.html

 la page d'accueil du catalogue, est identique à la première page
 https://books.toscrape.com/catalogue/category/books_1/page-1.html

 ensuite page-2, etc.

 Problème : récupérer la liste des livres

 Les livres s'affichent sur les pages dans le css

 exemple : <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>

 Il y a 50 pages, une stratégie peut être :
 - partir du site global
 - passer toutes les pages et récupérer toutes les url dans un dictionaire ou une liste
 -> concaténer tout ça pour avoir les url de tous les livres, soit url entières, soit url à concaténer à chaque fois


 Ensuite les données de chaque livre :
 - chaque url renvoie le code de la page
 - la description est au format suivant : "<meta name="description" content="
    It&#39;s hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein&#39;s humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It&#39;s hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein&#39;s humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon&#39;t you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here&#39;sGot it in for you. Shel, you never sounded so good. ...more
" />"

- les "product information" sont au format suivant :  <div class="sub-header">
        <h2>Product Information</h2>
    </div>
    <table class="table table-striped">

        <tr>
            <th>UPC</th><td>a897fe39b1053632</td>
        </tr>

        <tr>
            <th>Product Type</th><td>Books</td>
        </tr>



            <tr>
                <th>Price (excl. tax)</th><td>£51.77</td>
            </tr>

                <tr>
                    <th>Price (incl. tax)</th><td>£51.77</td>
                </tr>
                <tr>
                    <th>Tax</th><td>£0.00</td>
                </tr>

            <tr>
                <th>Availability</th>
                <td>In stock (22 available)</td>
            </tr>



            <tr>
                <th>Number of reviews</th>
                <td>0</td>
            </tr>

    </table>


