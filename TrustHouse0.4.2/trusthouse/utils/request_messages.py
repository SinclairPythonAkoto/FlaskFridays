def warning_message():
    """
    Returns a warning message if not the longitude & latitude has not been saved into the Maps table.
    Used for backend API and for user front end.
    For backend API reference both tuple indexes.
    For front end warning messages we only need to use the first tuple index : warning_message()[0]['Warning']

    EG.     warning_message()[1] = {'status': 199}
            warning_message()[1] = 200

            warning_message()[0] = warning message 
            warning_message()[1] = status code
    
    Returns a tuple of dictionaries with the warning message and status.
    """
    warning = {
        'Warning': 'Your address has been uploaded to Trust House, but the coordinates to your postcode could not be saved.'
    }
    status = {'status': 199}
    return warning, status


def error_message():
    """
    Returns an error message if unable to get the request.
    Used for backend API and for user front end messages.
    For backend API reference both tuple indexes.
    For front end error messages we only need to use the first tuple index : error_message()[0]['Error']

    EG.     error_message()[1] = {'status': 400}
            error_message()[1] = 400

            error_message()[0] = error message 
            error_message()[1] = status code
    
    Returns a tuple of dictionaries with the error message and status.
    """
    error = {
        'Error': 'Could not make your request. Please check and try again.'
    }
    status = {'status': 400}
    return error, status


def ok_message():
    """
    Returns a message to let the user the request went through.
    Used for backend API and front end messages.
    For backend API reference both tuple indexes.
    For front end OK messages we only need to use the first tuple index : ok_message()[0]['Success']

    EG.     ok_message()[2] = {'status': 200}
            ok_message()[2] = 200

            ok_message()[0] = good address & map details
            ok_message()[1] = good review 
            ok_message()[2] = status code 

    returns a tuple of dictionaries with OK messages and the status.
    """
    good_address = {
        'Success': 'Your address has been uploaded to Trust House.'
    }
    good_review = {
        'Success': 'Your review has been successfully uploaded to Trust House.'
    }
    status = {'status': 201}
    return good_address, good_review, status