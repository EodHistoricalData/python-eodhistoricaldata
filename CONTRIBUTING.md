# Contributing to Python EOD Historical Data

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to EOD Historical Data and its packages, 
which are hosted in the [EOD Orgnization](https://github.com/EodHistoricalData) on GitHub. 
These are mostly guidelines, not rules. Use your best judgment, 
and feel free to propose changes to this document in a pull request.


## Code of Conduct

Members of this project and everyone who participates in it are expected to behave well, specifically
not to use bad language when communicating with others, to be helpful and considerate. 

## I don't want to read this whole thing I just have a question!!!
 **Note:** submit an issue to ask a question

## How can I Contribute
#. Fork the repo, develop and test your code changes, add docs.
#. Make sure that your commit messages clearly describe the changes.
#. Send a pull request. (Please Read: `Faster Pull Request Reviews`_)

    ***************
    Adding Features
    ***************
    
    In order to add a feature:
    
    - The feature must be documented in both the API and narrative
      documentation.
    
    - The feature must work fully on the following Python versions:  
      3.7, 3.8, 3.9 and on both Linux and Windows.
    
    - The feature must not add unnecessary dependencies (where
      "unnecessary" is of course subjective, but new dependencies should
      be discussed).

    ****************************
    Using a Development Checkout
    ****************************
    
    You'll have to create a development environment using a Git checkout:
    
    - While logged into your GitHub account, navigate to the
      ``python-eodhistoricaldata`` `repo`_ on GitHub.
    
    - Fork and clone the ``python-eodhistoricaldata`` repository to your GitHub account by
      clicking the "Fork" button.
    
    - Clone your fork of ``python-eodhistoricaldata`` from your GitHub account to your local
      computer, substituting your account username and specifying the destination
      as ``python-eodhistoricaldata``.  E.g.::
    
       $ cd ${HOME}
       $ git clone git@github.com:USERNAME/python-eodhistoricaldata.git python-eodhistoricaldata
       $ cd python-eodhistoricaldata
       # Configure remotes such that you can pull changes from the python-eodhistoricaldata
       # repository into your local repository.
       $ git remote add upstream git@github.com:EodHistoricalData/python-eodhistoricaldata
       # fetch and merge changes from upstream into master
       $ git fetch upstream
       $ git merge upstream/master
    
    Now your local repo is set up such that you will push changes to your GitHub
    repo, from which you can submit a pull request.


    ************
    Coding Style
    ************
    
    - PEP8 compliance

    ************
    Running code Tests
    ************

    use the py.test command on the root of your local repo


  