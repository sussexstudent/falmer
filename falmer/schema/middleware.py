
import sys
import logging


class SentryMiddleware(object):
    def resolve(self, next, root, info, **args):
        try:
            return next(root, info, **args)
        except:
            err = sys.exc_info()
            logging.error(err)
            return err[1]
