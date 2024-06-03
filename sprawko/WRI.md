# WRI - laboratorium

Grupa laboratoryjna 105, realizacja stacjonarna 24L

Członkowie zespołu:

- Tomasz Owienko
- Bartosz Kisły
- Jakub Woźniak

- [x] Zdjęcie i nazwa robota
- [x] Zgrubny opis urządzeń
- [ ] Kalibracja
- [ ] Algorytm śledzenia linii (schemat blokowy?)
- [ ] Procedura doboru parametrów
- [ ] Algorytm transportera (schemat blokowy?)
- [ ] Problemy 
- [ ] Wnioski? xd


## Cel laboratorium

Celem laboratorium było zbudowanie robota z zestawu LEGO MINDSTORMS EV3 oraz oprogramowanie go pod kątem realizacji zadań przemieszczania się wzdłuż linii (*follow the line*) oraz transportu ładunku między zadanymi punktami.

## Opis konstrukcji

Zbudowany robot charakteryzuje się niskim środkiem ciężkości oraz bardzo szerokim rozstawem kół. Baza jezdna składa się z dwóch gumowych kół napędowych o szerokim bieżniku wysuniętych przed środek ciężkości oraz dwóch kół opartych na metalowych kulkach mających za zadanie stabilizować robota z tyłu. Niewiele przed osią obrotu umieszczono dwa sensory koloru na wysokości ok. 5mm od podłoża i w odległości ok 2cm pomiędzy sobą. Z tyłu robota umieszczono przycisk pozwalający zresetować zawarty w oprogramowaniu automat stanowy - finalnie okazał się on zbędny. Nad sensorami koloru umieszczono podłużny klocek LEGO (*"widły"*), który w zadaniu transportera służył do przesuwania ładunku po planszy bez podnoszenia go. Podczas realizacji zadania FTL zwiększono nieco rozstaw czujników koloru, co niestety nie zostało uchwycone na zdjęciach.

Nazwa robota: *Widłogon*

### FTL

<p float="left">
  <img src="./linia1.jpg" alt="Line Follower" width="300" />
  <img src="./linia2.jpg" alt="Line Follower" width="300" />
</p>

### Transporter

<p float="left">
  <img src="./towar1.jpg" alt="Transporter" width="300" />
  <img src="./towar2.jpg" alt="Transporter" width="300" />
</p>


## Oprogramowanie

Algorytm sterowanie robotem zaimplementowano w języku Python z wykorzystaniem biblioteki `python-ev3dev`.

TODO opisać algorytm


## Procedura kalibracji


### Link do repozytorium z kodem na Githubie

https://github.com/SNURTEL/24l-wri
### Opis konstrukcji

Podczas budowy robota wielokrotnie zmienialiśmy koncepcję i kształt, jednak przez wszystkie iteracje naszym głównym założeniem była "Prostota Wykonania". W ostatecznej iteracji zdecydowaliśmy się na konstrukcję, która oferowała jak najlepszą mobilność i kontrolę ruchu. Wybraliśmy robota z napędem na przednie koła o średnim rozmiarze i szerokim bieżniku, a jako tylne koła zastosowaliśmy metalowe kulki, inspirując się wózkami z supermarketów. Pozwoliło to na płynne skręcanie bez oporów i skomplikowania konstrukcji, jakie spowodowałoby użycie kół gumowych.

Nasze sensory kolorów zostały minimalnie wysunięte przed przednie koła, aby jak najbardziej pokrywały się z osią obrotu robota. Dodatkowo zdecydowaliśmy się na stosunkowo duże rozstawienie zarówno sensorów, jak i kół przednich, co ułatwiło utrzymywanie się na trasie podczas zakrętów.

Wierni naszemu mottu prostoty wykonania, zrezygnowaliśmy ze skomplikowanego i ruchomego podnośnika. Zamiast tego użyliśmy metody nadziewania towaru na widły, stąd nazwa naszego robota - Widłogon. Pozwoliło nam to znacząco uprościć sekwencję podnoszenia i opuszczania towaru. Wystarczyło nadziać towar na widły, a następnie po dojechaniu na pole o odpowiednim kolorze wycofać się, aby towar sam się zsunął. Dodatkowo na czas testowania i dostosowywania parametrów dodaliśmy do robota przycisk pozwalający nam resetować kod tak aby łatwiej było nam testować odbieranie i dostarczanie towaru.

Dzięki prostej konstrukcji bardzo łatwo było zmodyfikować naszego robota i usunąć dodatkowe obciążenie, jakim były widły, na czas wyścigu podążania po linii. Dzięki naszemu podejściu udało nam się osiągnąć najkrótszy czas w naszej grupie zarówno podczas wyścigu wykrywania linii (1:29:02), jak i transportu towaru (00:53:03).

### Tablica wyników
<p><img src="./wyniki.jpg" alt="Line Follower" width="300" /></p>

### Line Follower

<p float="left">
  <img src="./linia1.jpg" alt="Line Follower" width="300" />
  <img src="./linia2.jpg" alt="Line Follower" width="300" />
</p>

### Transporter

<p float="left">
  <img src="./towar1.jpg" alt="Transporter" width="300" />
  <img src="./towar2.jpg" alt="Transporter" width="300" />
</p>
