import requests
import json

class ParticleAPI:
    """
    Python wrapper for Particle API for flashing devices
    """
    __environment = None

    def __init__(self, env='production'):
        """
        Constructor

        :param env: 'production' or 'staging', used to determine url
        """
        self.__environment = env


    def particle_flash(self, device, file, access_token):
        """
        Calls the Particle API Flash endpoint

        :param device: string of device id, ex b1e2400...
        :param file: string of local filename
        :param access_token: string of Particle access token
        :return: True if update started, Fals otherwise
        """
        r = requests.put(self.__get_url()+'/v1/devices/'+device+'?access_token='+access_token,
                          files={
                              'file': open(file, 'rb')
                          })
        response = json.loads(r.text)
        if r.status_code == 200:
            return True
        else:
            return False

    def __get_url(self):
        """
        Gets the URL to send all commands

        :return: string of url to use based on specified environment
        """
        if self.__environment == "staging":
            return "https://api.staging.particle.io"
        else:
            return "https://api.particle.io"
