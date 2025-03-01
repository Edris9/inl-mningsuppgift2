# version tre 
pushade i denna länk:
https://github.com/Edris9/inl-mningsuppgift2

# Filar ligger i main 

# Vad jag har implementerat:

# TODOLIST:
- började med version ett bara för att fatta själva konceptet 
    byggde murar och försökte att röra på spelaren @ med wasd 
    för att version 1 är själva sturkturen eller byggnaden. 



## Spelets grunder
- Förflyttning med WASD-tangenter
- Samla föremål för poäng
- Undvik fällor och fiender

## Implementerade funktioner

### Grundfunktioner
- Spelplan med väggar och rörelsekontroller
- Inventory för upplockade föremål
- Poängsystem

### Avancerade funktioner för version 3 
1. **Fällor** - Ger -10 poäng när spelaren går på dem, ligger kvar
2. **Spade** - Kan användas en gång för att bryta ner en vägg
3. **Nycklar och kistor** - Nycklar används för att öppna kistor (100 poäng)
4. **Bördig jord** - Ny frukt/grönsak skapas efter var 25:e drag
5. **Exit** - Utgång som kräver att alla föremål är samlade för att vinna
6. **Jump** - Hoppa över rutor med "J"+riktning
7. **Grace period** - 5 drag utan poängavdrag efter upplockade föremål
8. **AI-fiender** - Fiender som jagar spelaren och ger -20 poäng vid kollision
9. **Bomber** - Placera bomber med "B", exploderar efter 3 drag
10. **Desarmera fällor** - Använd "T" för att desarmera närliggande fällor

## Kontroller
- WASD: Förflyttning
- J+WASD: Hoppa
- B: Placera bomb
- T: Desarmera fällor
- I: Visa inventory
- Q/X: Avsluta spelet

## Avancerade idéer
- Lägg till fler fiender och föremålstyper
- Skapa nivåsystem och svårighetsgrader