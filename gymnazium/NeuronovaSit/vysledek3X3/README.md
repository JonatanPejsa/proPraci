# Neuronová Síť pro Piškvorky

Tento projekt je implementace neuronové sítě, která hraje piškvorky proti hráči. Grafické rozhraní je vytvořeno pomocí knihovny pygame, a protihráč je implementována pomocí vlastní neuronové sítě.


## Struktura projektu

- `tic-tac-toe.py` – hlavní soubor, který spouští hru.
- `neuronovaSit.py` – definice neuronové sítě a vrstev.
- `obrazky/` – složka s obrázky.
- `data/` – obsahuje natrénované váhy a biasy neuronové sítě.


## Spuštění hry

Ujistšte se, že máte nainstalovaný Python a knihovny:
`pygame`
`numpy`
`pickle` (součást standardní knihovny Pythonu)
`random` (součást standardní knihovny Pythonu)
`math` (součást standardní knihovny Pythonu)

```bash
pip install pygame numpy
python tic-tac-toe.py