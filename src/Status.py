class StatusTypes:
    """
    Implements status types for the artifacts. Ensures no typo when using.
    """
    initialized = 'Initialized'
    gettingDependencies = 'Getting Dependencies'
    gettingUsages = 'Getting Usages'
    doneDependencies = 'Done Dependencies'
    doneUsages = 'Done Usages'
    verifyingDependency = 'Verifying Dependency'
    verifyingUsage = 'Verifying Usage'
    complete = 'Complete'
    error = 'Error'