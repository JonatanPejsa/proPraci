#ifndef __PROGTEST__
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <cctype>
#include <climits>
#include <cstdint>
#include <cassert>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <optional>
#include <memory>
#include <stdexcept>
#include <set>
#include <map>
#include <queue>
#include <deque>
#include <stack>
#include <unordered_map>
#include <unordered_set>
#include <string>        // pro std::string
#endif /* __PROGTEST__ */

struct Import{
  std::string nazev;
  std::vector<uint32_t> offsets;
};


struct Export{
  std::string nazev;
  uint32_t offset;
};


struct ObjectFile{
  std::vector<Import> importy;
  std::vector<Export> exporty;

  std::vector<uint8_t> code;
};


class CLinker
{
  public:
    CLinker()= default;
    ~CLinker()= default;
    
    CLinker & addFile ( const std::string & fileName )
    {
      
      std::ifstream vstup(fileName, std::ios::binary);
      if (!vstup) {
        throw std::runtime_error("neotevrel");
      }
      uint32_t pocet_exportu=0, pocet_importu= 0, velikost_kodu= 0;
      vstup.read(reinterpret_cast<char*>(&pocet_exportu), sizeof(pocet_exportu));
      if (!vstup) {
        throw std::runtime_error("hlavicka");
      }
      vstup.read(reinterpret_cast<char*>(&pocet_importu),sizeof(pocet_importu));
      if (!vstup) {
        throw std::runtime_error("hlavicka");
      }
      vstup.read(reinterpret_cast<char*>(&velikost_kodu),sizeof(velikost_kodu));
      if (!vstup) {
        throw std::runtime_error("hlavicka");
      }
      //std::cout<<pocet_exportu;
      //std::cout<<pocet_importu;
      //std::cout<<velikost_kodu;
      ObjectFile obj;
      for (uint32_t i = 0; i < pocet_exportu; i++){
        uint8_t delka;
        uint32_t offset;
        vstup.read(reinterpret_cast<char*>( &delka), 1);
        if (!vstup) {
          throw std::runtime_error("export");
        }
        std::string nazev (delka, '\0');
        vstup.read(&nazev[0], delka);
        if (!vstup) {
          throw std::runtime_error("export");
        }
        vstup.read(reinterpret_cast<char*>(&offset), sizeof(offset));
        if (!vstup) {
          throw std::runtime_error("export");
        }
        obj.exporty.push_back({nazev, offset});
      }
      for (uint32_t i=0; i<pocet_importu; i++){
        uint8_t delka;
        uint32_t reference;
        vstup.read(reinterpret_cast<char*>( &delka), 1);
        if (!vstup) {
          throw std::runtime_error("import");
        }
        std::string nazev(delka, '\0');
        vstup.read(&nazev[0], delka);
        if (!vstup) {
          throw std::runtime_error("import");
        }
        vstup.read(reinterpret_cast<char*>(&reference), sizeof(reference));
        if (!vstup) {
          throw std::runtime_error("import");
        }
        std::vector<uint32_t> offsets(reference);

        for (uint32_t j=0; j<reference; j++){
          uint32_t poz;
          vstup.read(reinterpret_cast<char*>(&poz), sizeof(poz));
          if (!vstup) {
            throw std::runtime_error("import");
          }
          offsets[j] = poz;
        }
        obj.importy.push_back({nazev, std::move(offsets)});
      }


      obj.code.resize(velikost_kodu);
      vstup.read(reinterpret_cast<char*>(obj.code.data()), velikost_kodu);
      if (!vstup){
        throw std::runtime_error("code");
      } 
      vstup.close();
      
      for (auto &i:obj.exporty){
        if (mapa.count(i.nazev)!=0){
          throw std::runtime_error("stejny");
        }
          
        mapa[i.nazev]= {pocet, i.offset};
      }
      objectFiles.push_back(std::move(obj));
      pocet++;
      return *this;
    }

    void linkOutput ( const std::string & fileName,
                      const std::string & entryPoint ){
       
      auto itEntry = mapa.find(entryPoint);
      if (itEntry == mapa.end()){
      throw std::runtime_error("nenealezeno");
      }
      auto vnitrni_funkce = bfs(entryPoint);

      std::vector<std::string> vnitrniFunkcePoporade;
      vnitrniFunkcePoporade.push_back(entryPoint);
      for (auto &i : vnitrni_funkce){
        if (i!=entryPoint){
          vnitrniFunkcePoporade.push_back(i);
        }
          
      }
      std::sort(vnitrniFunkcePoporade.begin() + 1, vnitrniFunkcePoporade.end());
      
      std::unordered_map<std::string, uint32_t> ofsety;
      uint32_t ted = 0;
      for (auto &jmeno:vnitrniFunkcePoporade) {
        auto [cislo, offset] = mapa[jmeno];
        ofsety[jmeno] = ted;
        ted += delkaFunkce(objectFiles[cislo], offset);
      }
      std::ofstream vystup(fileName, std::ios::binary);
      if (!vystup) {
        throw std::runtime_error("vystup");
      }

      for (auto &jmeno : vnitrniFunkcePoporade) {
        auto [cislo, offset] = mapa[jmeno];
        ObjectFile &obj = objectFiles[cislo];
        uint32_t delka = delkaFunkce(obj, offset);
        std::vector<uint8_t> blok(obj.code.begin()+offset, obj.code.begin()+offset+delka);
        uint8_t * zaklad = blok.data();
        for (auto &imp:obj.importy) {
          uint32_t target=ofsety[imp.nazev];
          for (auto poz : imp.offsets) {
            if (poz >= offset && poz+4 <= offset+delka) {
              uint32_t rel_poz = poz - offset;
              std::memcpy(zaklad + rel_poz, &target, sizeof(target));
            }
          }
        }
        vystup.write(reinterpret_cast<char*>(blok.data()), blok.size());
        if (!vystup) {
          throw std::runtime_error("vystup");
        }
      }
     }
    private:
      int pocet=0;
      std::vector<ObjectFile> objectFiles;
      std::unordered_map<std::string, std::pair<size_t, uint32_t>> mapa;
      
      std::unordered_set<std::string> bfs(const std::string &entryPoint)
      {
        std::unordered_set<std::string> navstiveneFunkce;
        std::queue<std::string> que;
        navstiveneFunkce.insert(entryPoint);
        que.push(entryPoint);
        while (!que.empty()) {
          std::string aktualniFunkce = que.front();
          que.pop();
          auto[indexSouboru, offsetFunkce]=mapa[aktualniFunkce];
          ObjectFile &objektovySoubor=objectFiles[indexSouboru];

          uint32_t delkaAktualniFunkce= delkaFunkce(objektovySoubor, offsetFunkce);
          for (const auto &importFunkce:objektovySoubor.importy) {
            for (uint32_t pozicePl:importFunkce.offsets) {
              bool uvnitr = ((pozicePl >= offsetFunkce) && (pozicePl+sizeof(uint32_t) <=offsetFunkce+delkaAktualniFunkce));
              if (!uvnitr) {
                continue;
              }
              else if (!mapa.count(importFunkce.nazev)){
                throw std::runtime_error("nedef");
              } 
              if (navstiveneFunkce.insert(importFunkce.nazev).second){
                que.push(importFunkce.nazev);
              }

            }
          }
        }
        return navstiveneFunkce;
      }
      uint32_t delkaFunkce(const ObjectFile &obj,uint32_t start)const
      {
        uint32_t end= obj.code.size();
        for (auto &i : obj.exporty) {
          if (i.offset>start && i.offset<end){
            end = i.offset;
          }
           
        }
        return end-start;
      }
    
};

#ifndef __PROGTEST__
int main ()
{
  CLinker () . addFile ( "0in0.o" ) . linkOutput ( "0out", "strlen" );

  CLinker () . addFile ( "1in0.o" ) . linkOutput ( "1out", "main" );

  CLinker () . addFile ( "2in0.o" ) . addFile ( "2in1.o" ) . linkOutput ( "2out", "main" );

  CLinker () . addFile ( "3in0.o" ) . addFile ( "3in1.o" ) . linkOutput ( "3out", "towersOfHanoi" );

  try
  {
    CLinker () . addFile ( "4in0.o" ) . addFile ( "4in1.o" ) . linkOutput ( "4out", "unusedFunc" );
    assert ( "missing an exception" == nullptr );
  }
  catch ( const std::runtime_error & e )
  {
    //std::cout<< e . what ();// Undefined symbol qsort
  }
  catch ( ... )
  {
    assert ( "invalid exception" == nullptr );
  }

  try
  {
    CLinker () . addFile ( "5in0.o" ) . linkOutput ( "5out", "main" );
    assert ( "missing an exception" == nullptr );
  }
  catch ( const std::runtime_error & e )
  {
    // e . what (): Duplicate symbol: printf
  }
  catch ( ... )
  {
    assert ( "invalid exception" == nullptr );
  }

  try
  {
    CLinker () . addFile ( "6in0.o" ) . linkOutput ( "6out", "strlen" );
    assert ( "missing an exception" == nullptr );
  }
  catch ( const std::runtime_error & e )
  {
    // e . what (): Cannot read input file
  }
  catch ( ... )
  {
    assert ( "invalid exception" == nullptr );
  }

  try
  {
    CLinker () . addFile ( "7in0.o" ) . linkOutput ( "7out", "strlen2" );
    assert ( "missing an exception" == nullptr );
  }
  catch ( const std::runtime_error & e )
  {
    // e . what (): Undefined symbol strlen2
  }
  catch ( ... )
  {
    assert ( "invalid exception" == nullptr );
  }

  return EXIT_SUCCESS;
}
#endif /* __PROGTEST__ */
