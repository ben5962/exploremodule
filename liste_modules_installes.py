import pip
import pkgutil
import inspect
import importlib
import six
import os
from pathlib import Path

installed_packages = pip.get_installed_distributions()


def getListOfModuleNamesInstalled():
    """ renvoie noms des modules installés """
    return [ m.name for m in pkgutil.iter_modules()]
    
def getListOfModuleNamesInstalledWithPip():
    """ renvoie nom des modules installés avec pip"""
    return [ m.key for m in installed_packages ]

def _PredModuleExiste(modulename):
    """ teste si un modulede nom machin existe """
    #return modulename in getListOfModuleNamesInstalled()
    return importlib.util.find_spec(modulename) is not None

def _DieIfModuleNameDoesNotExist(modulename):
    """ si module de tel nom existe pas meurt """
    if _PredModuleExiste(modulename):
        state = "MODULE_EXISTE"
    else:
        raise ValueError('il n existe pas de module de nom : ' + modulename)


def _DieIfModuleNameNotStringType(modulename):
    if not isinstance(modulename, six.string_types):
        raise ValueError('modulename attendu de type chaine etait de type ' + type(modulename) )
    else:
        state = "IMPORT_PAR_CHAINE_OK"


def _getInspectMembersFromModuleName(modulename,filtre=None):
    """ choppe la structure de liste renvoyée par inspect
        apres avoir controle le bon type de parametres passe"""
    filtres_fournis_par_inspect = [inspect.isfunction, inspect.isbuiltin, inspect.ismethod, inspect.isclass]

    

    def _DieIfFilterDoesNotExist(filtre):
        if filtre is not None and filtre not in filtres_fournis_par_inspect:
            raise ValueError('filtre souhaite n existe pas dans inspect')

    


    
    # execution principale
    _DieIfModuleNameNotStringType(modulename)
    _DieIfModuleNameDoesNotExist(modulename)
    module = importlib.import_module(modulename)
    liste_membres = inspect.getmembers(module,predicate=filtre)
    return liste_membres
  
        
    
    

def _getMembersWithLoading(modulename,filtre=None):
    """ retourne la liste des membres d un module
        avec inspect
        il reste a filter par type """
    return _getInspectMembersFromModuleName(modulename,filtre=None)
   

            
        

def getListOfFunctionsOfAModuleWithLoading(modulename):
    """ prend un nom de module
    renvoie la liste des noms de methodes qu il contient"""
    return _getInspectMembersFromModuleName(modulename, filtre=inspect.isfunction)


def getListOfMethodsOfAModuleWithLoading(modulename):
    """ prend un nom de module
    renvoie la liste des noms de sous modulesqu il contient"""
    return _getInspectMembersFromModuleName(modulename, filtre=inspect.ismethod)




def scanmodule(modulename):
    """ prend un nom de module,
        renvoie la liste des éléments visibles au chargement du module
        suggere un mode d emploi
    """

    def _DieIfNoAllObject(moduleobject):
        """doit mourir si pas de parametre __all__ dans le coeur du module """
        if not hasattr(moduleobject, '__all__'):
            raise ValueError('le module ' + repr(moduleobject) + ' n a pas d attribut __all__')
        
    def getAllObjectsNames(modulename):
        """si variable __all__ existe, elle suggere
            mode de fonctionnement du module"""
        _DieIfModuleNameNotStringType(modulename)
        _DieIfModuleNameDoesNotExist(modulename)
        moduleobject = importlib.import_module(modulename)
        #_DieIfNoAllObject(moduleobject)
        
        #all_mod_set = set(moduleobject.__all__)
        all_members_set = set([k for k, v in _getInspectMembersFromModuleName(modulename) ])
        
        #print("liste de all : " + repr(all_mod_set))
        
        print("liste de inspect sans customisation: ")
        print(all_members_set)

        print("#################")
        print("et maintenant avec tri")
        classes = []
        variables = []
        modules = []
        modules_mal_importes = []
        fonctions = []
        natifs = []
        autres = []
        
        print("nom du module : " + modulename )
        print("le fichier associe a cet import est : " + repr(moduleobject.__file__))
        print("package ou module?")
        nom_fichier_pointe_par_import = os.path.basename(moduleobject.__file__)
        nom_repertoire_parent_du_fichier_pointe_par_import = os.path.dirname(moduleobject.__file__)
        if nom_fichier_pointe_par_import == "__init__.py":
            print("package: import pointe vers pointe vers __init__.py")
        else:
            print("module : import pointe vers : " + nom_fichier_pointe_par_import)
        for k, v in _getInspectMembersFromModuleName(modulename):
            if k == '__builtins__' or k == '__doc__':
                continue
            #if k == '__file__':
            #    print(repr(v))
            # nan moduleobject.__file__
            if inspect.isclass(v):
                classes.append(k)
            elif inspect.ismodule(v):
                modules.append(k)
            elif inspect.isfunction(v):
                fonctions.append(k)
            elif inspect.isbuiltin(v):
                natifs.append(k)
            else:
                autres.append(k)

        # essayons de voir si des modules sont visibles depuis le chemin
        # mais mal importes
        if not modules:
            print("pas de module visible? verifions si présence de modules ou packages sans décla ds le rep")
            print("le fichier importé est : " + repr(moduleobject.__file__))
            # cherchons des repertoires sous le parent: ce sont des packages
            OBJET_PATH_PARENT = Path(nom_repertoire_parent_du_fichier_pointe_par_import)
            packages = [ p.name for p in OBJET_PATH_PARENT.iterdir() if p.is_dir() and p.name != '__pycache__' ]
            # cherchons des fichiers *.py
            modules_mal_importes = [ modl.name for modl in OBJET_PATH_PARENT.glob('./*.py') ]
        print("voici un premier classement: ")
        print("classes visibles : " + repr(classes))
        print("modules visibles : " + repr(modules))
        print("fonctions visibles : " + repr(fonctions))
        print("natifs visibles : " + repr(natifs))
        print("non classes : :" + repr(autres))

        if not modules:
            print("modules mal importes : " +  repr(modules_mal_importes))
            print("packages : " + repr(packages))
            for pkg in packages:
                getAllObjectsNames(modulename + '.' + pkg)
                                                                                                         
    getAllObjectsNames(modulename)
        

    
        

    
    
"""
print(
    type(installed_packages[0])
    +  " "
    + dir(installed_packages[0])
    )
"""
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
#print(installed_packages_list)
#print(installed_packages)



