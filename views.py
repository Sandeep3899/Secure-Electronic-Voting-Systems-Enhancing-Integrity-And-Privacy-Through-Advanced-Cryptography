import json
import os

import numpy as np
import requests
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.utils.text import slugify
from Pyfhel import PyCtxt, Pyfhel, PyPtxt
from Pyfhel.utils import Scheme_t

from account.views import account_login

from .models import Candidate, Position, Voter, Votes


def index(request):
    # This view redirects a user to the login page if they are not authenticated.
    if not request.user.is_authenticated:
        return account_login(request)
    context = {}
    # Commented out render, could display a login page.


def generate_ballot(display_controls=False):
    # This function generates the ballot for voting.
    # It retrieves all positions and orders them by priority.
    positions = Position.objects.order_by("priority").all()
    output = ""
    candidates_data = ""
    num = 1
    instruction = ""

    # Loops through each position (e.g., president, treasurer, etc.)
    for position in positions:
        name = position.name
        position_name = slugify(name)  # Converts the position name into a URL-friendly format.
        candidates = Candidate.objects.filter(position=position)  # Fetches candidates for this position.

        # Generates different input types (radio or checkbox) based on how many candidates can be selected.
        for candidate in candidates:
            if position.max_vote > 1:
                instruction = "You may select up to " + str(position.max_vote) + " candidates"
                input_box = (
                    '<input type="checkbox" value="'
                    + str(candidate.id)
                    + '" class="flat-red '
                    + position_name
                    + '" name="'
                    + position_name
                    + "[]"
                    + '">'
                )
            else:
                instruction = "Select only one candidate"
                input_box = (
                    '<input value="'
                    + str(candidate.id)
                    + '" type="radio" class="flat-red '
                    + position_name
                    + '" name="'
                    + position_name
                    + '">'
                )
            image = "/media/" + str(candidate.photo)  # Fetches the candidate’s photo from media storage.
            # Combines all the candidate data into an HTML structure.
            candidates_data = (
                candidates_data
                + "<li>"
                + input_box
                + '<button type="button" class="btn btn-primary btn-sm btn-flat clist platform" data-fullname="'
                + candidate.fullname
                + '" data-bio="'
                + candidate.bio
                + '"><i class="fa fa-search"></i> Platform</button><img src="'
                + image
                + '" height="100px" width="100px" class="clist"><span class="cname clist">'
                + candidate.fullname
                + "</span></li>"
            )
        
        # Handles the priority controls for moving a position up or down if the display_controls argument is True.
        up = ""
        if position.priority == 1:
            up = "disabled"
        down = ""
        if position.priority == positions.count():
            down = "disabled"
        
        # Generates the main HTML structure for the ballot, including candidate info and controls.
        output = (
            output
            + f"""<div class="row">	<div class="col-xs-12"><div class="box box-solid" id="{position.id}">
             <div class="box-header with-border">
            <h3 class="box-title"><b>{name}</b></h3>"""
        )

        if display_controls:
            output = (
                output
                + f""" <div class="pull-right box-tools">
        <button type="button" class="btn btn-default btn-sm moveup" data-id="{position.id}" {up}><i class="fa fa-arrow-up"></i> </button>
        <button type="button" class="btn btn-default btn-sm movedown" data-id="{position.id}" {down}><i class="fa fa-arrow-down"></i></button>
        </div>"""
            )

        # Finalizes the candidate section for each position.
        output = (
            output
            + f"""</div>
        <div class="box-body">
        <p>{instruction}
        <span class="pull-right">
        <button type="button" class="btn btn-success btn-sm btn-flat reset" data-desc="{position_name}"><i class="fa fa-refresh"></i> Reset</button>
        </span>
        </p>
        <div id="candidate_list">
        <ul>
        {candidates_data}
        </ul>
        </div>
        </div>
        </div>
        </div>
        </div>
        """
        )
        position.priority = num  # Updates position priority.
        position.save()
        num = num + 1
        candidates_data = ""
    
    # Returns the generated HTML ballot output.
    return output


def fetch_ballot(request):
    # Returns a ballot with display controls (used for admin view).
    output = generate_ballot(display_controls=True)
    return JsonResponse(output, safe=False)


def dashboard(request):
    # Renders the dashboard view where users can see their voting history if they have voted.
    user = request.user
    if user.voter.voted:  # Check if the user has already voted.
        context = {
            "my_votes": Votes.objects.filter(voter=user.voter),
        }
        return render(request, "voting/voter/result.html", context)
    else:
        # Redirect to the ballot if the user hasn't voted yet.
        return redirect(reverse("show_ballot"))


def show_ballot(request):
    # Displays the ballot to the voter, ensuring they haven't voted already.
    if request.user.voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse("voterDashboard"))
    ballot = generate_ballot(display_controls=False)
    context = {"ballot": ballot}
    return render(request, "voting/voter/ballot.html", context)


def preview_vote(request):
    # Handles previewing the votes selected by the user before final submission.
    if request.method != "POST":
        error = True
        response = "Please browse the system properly"
    else:
        output = ""
        form = dict(request.POST)  # Converts the POST data into a dictionary.
        print(form)
        form.pop("csrfmiddlewaretoken", None)  # Remove the CSRF token for easier processing.
        error = False
        data = []
        positions = Position.objects.all()  # Fetches all positions.

        # Loops through each position and generates a preview of the user's selected candidates.
        for position in positions:
            max_vote = position.max_vote
            pos = slugify(position.name)
            pos_id = position.id
            if position.max_vote > 1:
                this_key = pos + "[]"
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                if len(form_position) > max_vote:
                    error = True
                    response = (
                        "You can only choose "
                        + str(max_vote)
                        + " candidates for "
                        + position.name
                    )
                else:
                    # Generates HTML for the list of selected candidates for multi-choice positions.
                    start_tag = f"""
                       <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-8'>
                                <ul style='list-style-type:none; margin-left:-40px'>
                                
                    
                    """
                    end_tag = "</ul></span></div><hr/>"
                    data = ""
                    for form_candidate_id in form_position:
                        try:
                            candidate = Candidate.objects.get(
                                id=form_candidate_id, position=position
                            )
                            data += f"""
		                      	<li><i class="fa fa-check-square-o"></i> {candidate.fullname}</li>
                            """
                        except:
                            error = True
                            response = "Please, browse the system properly"
                    output += start_tag + data + end_tag
            else:
                this_key = pos
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                # Generates HTML for the list of selected candidates for single-choice positions.
                try:
                    form_position = form_position[0]
                    candidate = Candidate.objects.get(
                        position=position, id=form_position
                    )
                    output += f"""
                            <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-8'><i class="fa fa-check-circle-o"></i> {candidate.fullname}</span>
		                    </div>
                      <hr/>
                    """
                except Exception as e:
                    error = True
                    response = "Please, browse the system properly"
    # Returns the preview list and any errors as a JSON response.
    context = {"error": error, "list": output}
    return JsonResponse(context, safe=False)


def submit_ballot(request):
    # Handles the final submission of a ballot by the voter.
    if request.method != "POST":
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse("show_ballot"))

    # Verifies if the voter has voted already.
    voter = request.user.voter
    if voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse("voterDashboard"))

    form = dict(request.POST)
    print(form)
    form.pop("csrfmiddlewaretoken", None)  # Removes CSRF token for processing.
    form.pop("submit_vote", None)  # Removes the submit button input.

    # Ensures that at least one vote is cast.
    if len(form.keys()) < 1:
        messages.error(request, "Please select at least one candidate")
        return redirect(reverse("show_ballot"))
    
    # Loops through the selected candidates and processes the vote.
    positions = Position.objects.all()
    form_count = 0
    for position in positions:
        max_vote = position.max_vote
        pos = slugify(position.name)
        pos_id = position.id
        if position.max_vote > 1:
            this_key = pos + "[]"
            form_position = form.get(this_key)
            if form_position is None:
                continue
            if len(form_position) > max_vote:
                messages.error(
                    request,
                    "You can only choose "
                    + str(max_vote)
                    + " candidates for "
                    + position.name,
                )
                return redirect(reverse("show_ballot"))
            else:
                for form_candidate_id in form_position:
                    form_count += 1
                    try:
                        # Fetches the selected candidate and encrypts the vote using Pyfhel homomorphic encryption.
                        candidate = Candidate.objects.get(
                            id=form_candidate_id, position=position
                        )
                        voter_fhel = Pyfhel()
                        voter_fhel.load_context(voter.hash_id + "/context")
                        voter_fhel.load_public_key(voter.hash_id + "/pub.key")
                        voter_fhel.load_secret_key(voter.hash_id + "/sec.key")

                        voter.voted_to = voter_fhel.encrypt(
                            np.array([candidate.id])
                        ).to_bytes()
                        voter.save()

                        # Updates the candidate's vote count using homomorphic encryption.
                        candidate_fhel = Pyfhel()
                        candidate_fhel.load_context(candidate.hash_id + "/context")
                        candidate_fhel.load_public_key(candidate.hash_id + "/pub.key")
                        candidate_fhel.load_secret_key(candidate.hash_id + "/sec.key")
                        candidate.vote_cound = candidate_fhel.add(
                            PyCtxt(pyfhel=candidate_fhel, bytestring=candidate.vote_cound),
                            candidate_fhel.encryptInt(np.array([1], dtype=np.int64)),
                        ).to_bytes()
                        candidate.save()
                    except Exception as e:
                        messages.error(
                            request, "Please, browse the system properly " + str(e)
                        )
                        return redirect(reverse("show_ballot"))
        else:
            this_key = pos
            form_position = form.get(this_key)
            if form_position is None:
                continue
            # Processes the vote for single-choice positions.
            form_count += 1
            try:
                form_position = form_position[0]
                candidate = Candidate.objects.get(position=position, id=form_position)

                # Encrypts and saves the voter's choice using Pyfhel.
                voter_fhel = Pyfhel()
                voter_fhel.load_context(voter.hash_id + "/context")
                voter_fhel.load_public_key(voter.hash_id + "/pub.key")
                voter_fhel.load_secret_key(voter.hash_id + "/sec.key")

                voter.voted_to = voter_fhel.encrypt(
                    np.array([candidate.id], dtype=np.int64)
                ).to_bytes()
                voter.save()

                # Adds one vote to the candidate using homomorphic encryption.
                candidate_fhel = Pyfhel()
                candidate_fhel.load_context(candidate.hash_id + "/context")
                candidate_fhel.load_public_key(candidate.hash_id + "/pub.key")
                candidate_fhel.load_secret_key(candidate.hash_id + "/sec.key")
                candidate.vote_cound = candidate_fhel.add(
                    PyCtxt(pyfhel=candidate_fhel, bytestring=candidate.vote_cound),
                    candidate_fhel.encryptInt(np.array([1], dtype=np.int64)),
                ).to_bytes()

                candidate.save()
            except Exception as e:
                print(str(e))
                messages.error(request, "Please, browse the system properly " + str(e))
                return redirect(reverse("show_ballot"))
    
    # Marks the voter as having voted and redirects them to the dashboard.
    voter.voted = True
    voter.save()
    messages.success(request, "Thanks for voting")
    return redirect(reverse("voterDashboard"))


def account_download_key(request):
    # Allows the user to download their public key.
    if request.method != "POST":
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse("show_ballot"))
    if not request.user.is_authenticated:
        return account_login(request)
    voter = request.user.voter
    file_path = voter.hash_id + "/pub.key"
    
    # Checks if the public key file exists and returns it as a file download response.
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = (
            f'attachment; filename="{os.path.basename(file_path)}"'
        )
        return response
    else:
        return render(request, "error.html", {"message": "File not found."})
    return redirect(reverse("show_ballot"))


def viewvote(request):
    # Allows a user to view the details of the vote they cast.
    if request.method != "POST":
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse("dashboard"))

    # Fetches the voter and decrypts the vote using Pyfhel to retrieve the candidate they voted for.
    voter = request.user.voter
    print("\n", voter)
    context = {}
    if voter.voted:
        voter_fhel = Pyfhel()
        voter_fhel.load_context(voter.hash_id + "/context")
        voter_fhel.load_public_key(voter.hash_id + "/pub.key")
        voter_fhel.load_secret_key(voter.hash_id + "/sec.key")

        # Decrypts the vote and retrieves the candidate's information.
        Candidate_id = voter_fhel.decrypt(
            PyCtxt(pyfhel=voter_fhel, bytestring=voter.voted_to)
        )[0]
        candidate = Candidate.objects.get(id=Candidate_id)
        context = {
            "name": candidate.fullname,
            "image": "/media/" + str(candidate.photo),
            "desc": candidate.bio,
        }
        print(context)

    # Returns the candidate details as a JSON response.
    return JsonResponse(context)

