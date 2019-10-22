// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME bindIdict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualifies STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "src/classes.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *AngCoeff_Dictionary();
   static void AngCoeff_TClassManip(TClass*);
   static void *new_AngCoeff(void *p = 0);
   static void *newArray_AngCoeff(Long_t size, void *p);
   static void delete_AngCoeff(void *p);
   static void deleteArray_AngCoeff(void *p);
   static void destruct_AngCoeff(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::AngCoeff*)
   {
      ::AngCoeff *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::AngCoeff));
      static ::ROOT::TGenericClassInfo 
         instance("AngCoeff", "AngCoeff.hpp", 17,
                  typeid(::AngCoeff), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &AngCoeff_Dictionary, isa_proxy, 4,
                  sizeof(::AngCoeff) );
      instance.SetNew(&new_AngCoeff);
      instance.SetNewArray(&newArray_AngCoeff);
      instance.SetDelete(&delete_AngCoeff);
      instance.SetDeleteArray(&deleteArray_AngCoeff);
      instance.SetDestructor(&destruct_AngCoeff);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::AngCoeff*)
   {
      return GenerateInitInstanceLocal((::AngCoeff*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::AngCoeff*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *AngCoeff_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::AngCoeff*)0x0)->GetClass();
      AngCoeff_TClassManip(theClass);
   return theClass;
   }

   static void AngCoeff_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *dataObs_Dictionary();
   static void dataObs_TClassManip(TClass*);
   static void *new_dataObs(void *p = 0);
   static void *newArray_dataObs(Long_t size, void *p);
   static void delete_dataObs(void *p);
   static void deleteArray_dataObs(void *p);
   static void destruct_dataObs(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::dataObs*)
   {
      ::dataObs *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::dataObs));
      static ::ROOT::TGenericClassInfo 
         instance("dataObs", "dataObs.hpp", 20,
                  typeid(::dataObs), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &dataObs_Dictionary, isa_proxy, 4,
                  sizeof(::dataObs) );
      instance.SetNew(&new_dataObs);
      instance.SetNewArray(&newArray_dataObs);
      instance.SetDelete(&delete_dataObs);
      instance.SetDeleteArray(&deleteArray_dataObs);
      instance.SetDestructor(&destruct_dataObs);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::dataObs*)
   {
      return GenerateInitInstanceLocal((::dataObs*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::dataObs*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *dataObs_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::dataObs*)0x0)->GetClass();
      dataObs_TClassManip(theClass);
   return theClass;
   }

   static void dataObs_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *defineHarmonics_Dictionary();
   static void defineHarmonics_TClassManip(TClass*);
   static void *new_defineHarmonics(void *p = 0);
   static void *newArray_defineHarmonics(Long_t size, void *p);
   static void delete_defineHarmonics(void *p);
   static void deleteArray_defineHarmonics(void *p);
   static void destruct_defineHarmonics(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::defineHarmonics*)
   {
      ::defineHarmonics *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::defineHarmonics));
      static ::ROOT::TGenericClassInfo 
         instance("defineHarmonics", "defineHarmonics.hpp", 16,
                  typeid(::defineHarmonics), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &defineHarmonics_Dictionary, isa_proxy, 4,
                  sizeof(::defineHarmonics) );
      instance.SetNew(&new_defineHarmonics);
      instance.SetNewArray(&newArray_defineHarmonics);
      instance.SetDelete(&delete_defineHarmonics);
      instance.SetDeleteArray(&deleteArray_defineHarmonics);
      instance.SetDestructor(&destruct_defineHarmonics);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::defineHarmonics*)
   {
      return GenerateInitInstanceLocal((::defineHarmonics*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::defineHarmonics*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *defineHarmonics_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::defineHarmonics*)0x0)->GetClass();
      defineHarmonics_TClassManip(theClass);
   return theClass;
   }

   static void defineHarmonics_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *defineSystWeight_Dictionary();
   static void defineSystWeight_TClassManip(TClass*);
   static void delete_defineSystWeight(void *p);
   static void deleteArray_defineSystWeight(void *p);
   static void destruct_defineSystWeight(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::defineSystWeight*)
   {
      ::defineSystWeight *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::defineSystWeight));
      static ::ROOT::TGenericClassInfo 
         instance("defineSystWeight", "defineSystWeight.hpp", 16,
                  typeid(::defineSystWeight), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &defineSystWeight_Dictionary, isa_proxy, 4,
                  sizeof(::defineSystWeight) );
      instance.SetDelete(&delete_defineSystWeight);
      instance.SetDeleteArray(&deleteArray_defineSystWeight);
      instance.SetDestructor(&destruct_defineSystWeight);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::defineSystWeight*)
   {
      return GenerateInitInstanceLocal((::defineSystWeight*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::defineSystWeight*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *defineSystWeight_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::defineSystWeight*)0x0)->GetClass();
      defineSystWeight_TClassManip(theClass);
   return theClass;
   }

   static void defineSystWeight_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *getACValues_Dictionary();
   static void getACValues_TClassManip(TClass*);
   static void delete_getACValues(void *p);
   static void deleteArray_getACValues(void *p);
   static void destruct_getACValues(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::getACValues*)
   {
      ::getACValues *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::getACValues));
      static ::ROOT::TGenericClassInfo 
         instance("getACValues", "getACValues.hpp", 17,
                  typeid(::getACValues), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &getACValues_Dictionary, isa_proxy, 4,
                  sizeof(::getACValues) );
      instance.SetDelete(&delete_getACValues);
      instance.SetDeleteArray(&deleteArray_getACValues);
      instance.SetDestructor(&destruct_getACValues);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::getACValues*)
   {
      return GenerateInitInstanceLocal((::getACValues*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::getACValues*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *getACValues_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::getACValues*)0x0)->GetClass();
      getACValues_TClassManip(theClass);
   return theClass;
   }

   static void getACValues_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *getAccMap_Dictionary();
   static void getAccMap_TClassManip(TClass*);
   static void delete_getAccMap(void *p);
   static void deleteArray_getAccMap(void *p);
   static void destruct_getAccMap(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::getAccMap*)
   {
      ::getAccMap *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::getAccMap));
      static ::ROOT::TGenericClassInfo 
         instance("getAccMap", "getAccMap.hpp", 17,
                  typeid(::getAccMap), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &getAccMap_Dictionary, isa_proxy, 4,
                  sizeof(::getAccMap) );
      instance.SetDelete(&delete_getAccMap);
      instance.SetDeleteArray(&deleteArray_getAccMap);
      instance.SetDestructor(&destruct_getAccMap);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::getAccMap*)
   {
      return GenerateInitInstanceLocal((::getAccMap*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::getAccMap*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *getAccMap_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::getAccMap*)0x0)->GetClass();
      getAccMap_TClassManip(theClass);
   return theClass;
   }

   static void getAccMap_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *getWeights_Dictionary();
   static void getWeights_TClassManip(TClass*);
   static void *new_getWeights(void *p = 0);
   static void *newArray_getWeights(Long_t size, void *p);
   static void delete_getWeights(void *p);
   static void deleteArray_getWeights(void *p);
   static void destruct_getWeights(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::getWeights*)
   {
      ::getWeights *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::getWeights));
      static ::ROOT::TGenericClassInfo 
         instance("getWeights", "getWeights.hpp", 20,
                  typeid(::getWeights), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &getWeights_Dictionary, isa_proxy, 4,
                  sizeof(::getWeights) );
      instance.SetNew(&new_getWeights);
      instance.SetNewArray(&newArray_getWeights);
      instance.SetDelete(&delete_getWeights);
      instance.SetDeleteArray(&deleteArray_getWeights);
      instance.SetDestructor(&destruct_getWeights);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::getWeights*)
   {
      return GenerateInitInstanceLocal((::getWeights*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::getWeights*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *getWeights_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::getWeights*)0x0)->GetClass();
      getWeights_TClassManip(theClass);
   return theClass;
   }

   static void getWeights_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *templateBuilder_Dictionary();
   static void templateBuilder_TClassManip(TClass*);
   static void *new_templateBuilder(void *p = 0);
   static void *newArray_templateBuilder(Long_t size, void *p);
   static void delete_templateBuilder(void *p);
   static void deleteArray_templateBuilder(void *p);
   static void destruct_templateBuilder(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::templateBuilder*)
   {
      ::templateBuilder *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::templateBuilder));
      static ::ROOT::TGenericClassInfo 
         instance("templateBuilder", "templateBuilder.hpp", 20,
                  typeid(::templateBuilder), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &templateBuilder_Dictionary, isa_proxy, 4,
                  sizeof(::templateBuilder) );
      instance.SetNew(&new_templateBuilder);
      instance.SetNewArray(&newArray_templateBuilder);
      instance.SetDelete(&delete_templateBuilder);
      instance.SetDeleteArray(&deleteArray_templateBuilder);
      instance.SetDestructor(&destruct_templateBuilder);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::templateBuilder*)
   {
      return GenerateInitInstanceLocal((::templateBuilder*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::templateBuilder*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *templateBuilder_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::templateBuilder*)0x0)->GetClass();
      templateBuilder_TClassManip(theClass);
   return theClass;
   }

   static void templateBuilder_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_AngCoeff(void *p) {
      return  p ? new(p) ::AngCoeff : new ::AngCoeff;
   }
   static void *newArray_AngCoeff(Long_t nElements, void *p) {
      return p ? new(p) ::AngCoeff[nElements] : new ::AngCoeff[nElements];
   }
   // Wrapper around operator delete
   static void delete_AngCoeff(void *p) {
      delete ((::AngCoeff*)p);
   }
   static void deleteArray_AngCoeff(void *p) {
      delete [] ((::AngCoeff*)p);
   }
   static void destruct_AngCoeff(void *p) {
      typedef ::AngCoeff current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::AngCoeff

namespace ROOT {
   // Wrappers around operator new
   static void *new_dataObs(void *p) {
      return  p ? new(p) ::dataObs : new ::dataObs;
   }
   static void *newArray_dataObs(Long_t nElements, void *p) {
      return p ? new(p) ::dataObs[nElements] : new ::dataObs[nElements];
   }
   // Wrapper around operator delete
   static void delete_dataObs(void *p) {
      delete ((::dataObs*)p);
   }
   static void deleteArray_dataObs(void *p) {
      delete [] ((::dataObs*)p);
   }
   static void destruct_dataObs(void *p) {
      typedef ::dataObs current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::dataObs

namespace ROOT {
   // Wrappers around operator new
   static void *new_defineHarmonics(void *p) {
      return  p ? new(p) ::defineHarmonics : new ::defineHarmonics;
   }
   static void *newArray_defineHarmonics(Long_t nElements, void *p) {
      return p ? new(p) ::defineHarmonics[nElements] : new ::defineHarmonics[nElements];
   }
   // Wrapper around operator delete
   static void delete_defineHarmonics(void *p) {
      delete ((::defineHarmonics*)p);
   }
   static void deleteArray_defineHarmonics(void *p) {
      delete [] ((::defineHarmonics*)p);
   }
   static void destruct_defineHarmonics(void *p) {
      typedef ::defineHarmonics current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::defineHarmonics

namespace ROOT {
   // Wrapper around operator delete
   static void delete_defineSystWeight(void *p) {
      delete ((::defineSystWeight*)p);
   }
   static void deleteArray_defineSystWeight(void *p) {
      delete [] ((::defineSystWeight*)p);
   }
   static void destruct_defineSystWeight(void *p) {
      typedef ::defineSystWeight current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::defineSystWeight

namespace ROOT {
   // Wrapper around operator delete
   static void delete_getACValues(void *p) {
      delete ((::getACValues*)p);
   }
   static void deleteArray_getACValues(void *p) {
      delete [] ((::getACValues*)p);
   }
   static void destruct_getACValues(void *p) {
      typedef ::getACValues current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::getACValues

namespace ROOT {
   // Wrapper around operator delete
   static void delete_getAccMap(void *p) {
      delete ((::getAccMap*)p);
   }
   static void deleteArray_getAccMap(void *p) {
      delete [] ((::getAccMap*)p);
   }
   static void destruct_getAccMap(void *p) {
      typedef ::getAccMap current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::getAccMap

namespace ROOT {
   // Wrappers around operator new
   static void *new_getWeights(void *p) {
      return  p ? new(p) ::getWeights : new ::getWeights;
   }
   static void *newArray_getWeights(Long_t nElements, void *p) {
      return p ? new(p) ::getWeights[nElements] : new ::getWeights[nElements];
   }
   // Wrapper around operator delete
   static void delete_getWeights(void *p) {
      delete ((::getWeights*)p);
   }
   static void deleteArray_getWeights(void *p) {
      delete [] ((::getWeights*)p);
   }
   static void destruct_getWeights(void *p) {
      typedef ::getWeights current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::getWeights

namespace ROOT {
   // Wrappers around operator new
   static void *new_templateBuilder(void *p) {
      return  p ? new(p) ::templateBuilder : new ::templateBuilder;
   }
   static void *newArray_templateBuilder(Long_t nElements, void *p) {
      return p ? new(p) ::templateBuilder[nElements] : new ::templateBuilder[nElements];
   }
   // Wrapper around operator delete
   static void delete_templateBuilder(void *p) {
      delete ((::templateBuilder*)p);
   }
   static void deleteArray_templateBuilder(void *p) {
      delete [] ((::templateBuilder*)p);
   }
   static void destruct_templateBuilder(void *p) {
      typedef ::templateBuilder current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::templateBuilder

namespace {
  void TriggerDictionaryInitialization_dict_Impl() {
    static const char* headers[] = {
"0",
0
    };
    static const char* includePaths[] = {
"interface/",
"../",
"/cvmfs/sft-nightlies.cern.ch/lcg/nightlies/dev3/Tue/ROOT/HEAD/x86_64-centos7-gcc62-opt/include/",
"/scratchssd/emanca/wproperties-analysis/signalAnalysis/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "dict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$interface/AngCoeff.hpp")))  AngCoeff;
class __attribute__((annotate("$clingAutoload$interface/dataObs.hpp")))  dataObs;
class __attribute__((annotate("$clingAutoload$interface/defineHarmonics.hpp")))  defineHarmonics;
class __attribute__((annotate("$clingAutoload$interface/defineSystWeight.hpp")))  defineSystWeight;
class __attribute__((annotate("$clingAutoload$interface/getACValues.hpp")))  getACValues;
class __attribute__((annotate("$clingAutoload$interface/getAccMap.hpp")))  getAccMap;
class __attribute__((annotate("$clingAutoload$interface/getWeights.hpp")))  getWeights;
class __attribute__((annotate("$clingAutoload$interface/templateBuilder.hpp")))  templateBuilder;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "dict dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
//#include "interface/TH1weightsHelper.hpp"
//#include "interface/TH2weightsHelper.hpp"
//#include "interface/TH3weightsHelper.hpp"
#include "interface/module.hpp"
#include "interface/AngCoeff.hpp"
#include "interface/dataObs.hpp"
#include "interface/defineHarmonics.hpp"
#include "interface/defineSystWeight.hpp"
#include "interface/getACValues.hpp"
#include "interface/getAccMap.hpp"
#include "interface/getWeights.hpp"
#include "interface/templateBuilder.hpp"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"AngCoeff", payloadCode, "@",
"dataObs", payloadCode, "@",
"defineHarmonics", payloadCode, "@",
"defineSystWeight", payloadCode, "@",
"getACValues", payloadCode, "@",
"getAccMap", payloadCode, "@",
"getWeights", payloadCode, "@",
"templateBuilder", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("dict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_dict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_dict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_dict() {
  TriggerDictionaryInitialization_dict_Impl();
}
