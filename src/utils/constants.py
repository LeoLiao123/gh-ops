from ..features import PRAnalyzer, CodeReviewer, DependencyChecker, StatsGenerator

FEATURES = {
    '1': ('Analyze PR Changes', PRAnalyzer),
    '2': ('Review Code Quality', CodeReviewer),
    '3': ('Check Dependencies', DependencyChecker),
    '4': ('Generate PR Statistics', StatsGenerator),
    '5': ('Exit', None)
}
