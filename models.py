from django.db import models
from account.models import CustomUser  # Importing the CustomUser model to link with the Voter model.

# Voter model to store details of individual voters.
class Voter(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Links each voter to a user account in the CustomUser model. One-to-one relationship.
    # If the user is deleted, their associated Voter profile will also be deleted.

    phone = models.CharField(max_length=11, unique=True)  # Used for OTP
    # Stores the voter's phone number. It's limited to 11 characters and must be unique.

    verified = models.BooleanField(default=False)
    # A boolean field that indicates whether the voter is verified (e.g., through OTP verification). Defaults to False.

    voted = models.BooleanField(default=False)
    # A boolean field indicating whether the voter has voted. Defaults to False, and changes to True once they vote.

    hash_id = models.CharField(max_length=10, unique=True, null=False)
    # A unique identifier for the voter, used in encryption and other security measures. It must be unique and cannot be null.

    voted_to = models.BinaryField(null=True)
    # Stores the encrypted data of the candidate(s) the voter voted for, stored in binary format.

    ssn = models.CharField(max_length=11)
    # Stores the voter's Social Security Number (SSN) or equivalent, using a CharField with a max length of 11.

    encode_ssn = models.BinaryField(null=True)
    # Stores an encrypted version of the voter's SSN in binary format. Can be null.

    dob = models.DateField(null=True)
    # Stores the voter's date of birth (dob). This field can be null.

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name
    # String representation of the Voter model, showing the voter's last name and first name.

# Position model to define positions (e.g., President, Treasurer) that voters can vote for.
class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # Name of the position (e.g., President). It is unique, meaning two positions cannot have the same name.

    max_vote = models.IntegerField()
    # Maximum number of votes allowed for this position (e.g., if voters can select more than one candidate).

    priority = models.IntegerField()
    # Determines the order in which positions appear on the ballot (e.g., a higher priority means it appears first).

    def __str__(self):
        return self.name
    # String representation of the Position model, returning the name of the position.

# Candidate model to define individual candidates for specific positions.
class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    # Stores the candidate's full name.

    photo = models.ImageField(upload_to="candidates")
    # Stores a photo of the candidate. The image will be uploaded to the "candidates" folder in media storage.

    bio = models.TextField()
    # A text field to store the candidate's biography or background information.

    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # Links the candidate to a specific position (e.g., President, Treasurer). If the position is deleted, all associated candidates will also be deleted (on_delete=models.CASCADE).

    vote_cound = models.BinaryField(null=True)
    # Stores the candidate's encrypted vote count in binary format. Can be null.

    hash_id = models.CharField(max_length=16, unique=True, null=False)
    # A unique identifier for the candidate, similar to the voter's hash ID, used for encryption or other security measures.

    def __str__(self):
        return self.fullname
    # String representation of the Candidate model, returning the candidate's full name.

# Votes model to track individual votes.
class Votes(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    # Links each vote to a voter. If the voter is deleted, all their votes are deleted (on_delete=models.CASCADE).

    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # Links each vote to a specific position. If the position is deleted, the associated votes are also deleted.

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # Links each vote to a specific candidate. If the candidate is deleted, the associated votes are deleted.

