def add_vote_counts(features, user_id):
    """
    Adds vote count to serialized features data
    :param features:
    :param user_id:
    :return: Updated serialized features
    """
    for feature in features:
        total_votes = len(feature['user_votes'])
        feature['votes'] = total_votes

        # Set user vote to True or False
        set_user_vote(feature, user_id)

    return features


def set_user_vote(feature, user_id):
    """
    Sets user_votes to True if user_id in votes array
    Set users vote
    :param feature:
    :param user_id:
    :return:
    """
    total_votes = len(feature['user_votes'])
    if total_votes:
        # Set all feature voted by user to true
        for votes in feature['user_votes']:
            if votes['user_id'] == user_id:
                feature['user_votes'] = True
                break

    if not (feature['user_votes'] == True):
        feature['user_votes'] = False

    return feature
