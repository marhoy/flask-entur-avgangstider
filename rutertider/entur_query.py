import requests
import random


# For testing of queries, use this page:
# https://api.entur.org/doc/shamash-journeyplanner/


def create_departure_query(stop_id, max_departures=5):
    """Create a GraphQL query, finding all departures for a specific stop_id

    Args:
        stop_id: The stop_id you want departures for
        max_departures: The maximum number of departures to return

    Returns:
        A GraphQL query
    """
    departure_query = """
    {
      stopPlace(id: "STOP_PLACE" ) {
        name
        estimatedCalls(numberOfDepartures: MAX_DEPARTURES ) {
          quay {
            id
            description
          }
          expectedArrivalTime
          actualArrivalTime
          expectedDepartureTime
          actualDepartureTime
          realtime
          realtimeState
          destinationDisplay {
            frontText
          }
          serviceJourney {
            line {
              publicCode
              presentation {
                colour
                textColour
              }
            }
          }
        }
      }
    }
    """.replace('STOP_PLACE', stop_id).\
        replace('MAX_DEPARTURES', str(max_departures))
    return departure_query


def create_situation_query(line_id):
    """Create a GraphQL query, finding all situations for a specific line_id

    Args:
        line_id: The line_id you want situations for

    Returns:
        A GraphQL query
    """
    situation_query = """
    {
      line(id: "LINE_ID") {
        id
        situations {
          summary {
            value
          }
          description {
            value
          }
          detail {
            value
          }
          validityPeriod {
            startTime
            endTime
          }
        }
      }
    }
    """.replace('LINE_ID', line_id)
    return situation_query


def journey_planner_api(query):
    """Query the Entur Journey Planner API

    Args:
        query: A string with the GraphQL query

    Returns:
        A requests response object
    """
    query_url = 'https://api.entur.io/journey-planner/v2/graphql'
    headers = {'ET-Client-Name': 'flask - avgangstider_{:03}'.format(
        random.randint(0, 999))}
    response = requests.post(query_url, headers=headers, json={'query': query})
    response.raise_for_status()
    return response
