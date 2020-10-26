# FrMaya

FrMaya is Maya Python package and is an ongoing project. 
One of its feature is tool distribution through **MayaMenubar** folder or 
any folder registered in **FR_MYMENUBAR** environment, 
artist can drop script either python or mel in the folder and it will automatically updated on maya menubar. 
FrMaya also has built in tool, from general purpose, modeling, rigging, etc.


## Installing
These instructions will get you a copy of FrMaya up and running on your machine.

> 1. Download ZIP from either master branch, latest release or use git clone.
> 2. Navigate inside FrMaya root project.
> 3. Drag and drop install.mel into your maya viewport.
> 4. Click install, choose either local or remote.
> 5. Restart maya.
> 6. Now FrMaya menubar should be showed on your maya

## Maya version

Tested and used on 2016, 2017, 2018.
On maya 2016 the update system wont work because python security issues.

## Structure
FrMaya package structure description.
```
├── FrMaya
│   ├── core
│   ├── tools
│   ├── utility
│   └── vendor
└── ...
```
- core

  Collection of FrMaya function,
  many useful function is not exposed to GUI can be accessed through here.
- tools

  Collection of FrMaya tools.
- utility

  Utility function used for core and tools package.
- vendor

  3rd party package and module in FrMaya.

## Authors

* **Muhammad Fredo** - *Initial work* - [muhammadfredo](https://github.com/muhammadfredo)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* cometJointOrient from [Michael B. Comet](http://www.comet-cartoons.com/)
* WpRename from [William Petruccelli](https://www.highend3d.com/maya/script/wp-rename-for-maya)
