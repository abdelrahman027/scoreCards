from django.shortcuts import render, redirect
from django.http import JsonResponse

# Initialize global variables for the first request
def initialize_session(request):
    if 'questions_array' not in request.session:
        request.session['questions_array'] = [
            ["Producing ideas is one of my natural assets.","I am apt to get too caught up in ideas that occur to me and so lose track of what is happening.","I can be counted on to contribute something original.","I prefer to avoid the obvious and to open up lines that have not been explored.","I can find an opportunity to stretch my imagination.","I would feel like devising a solution of my own and then trying to sell it to the group.","I am sometimes poor at putting across complex points that occur to me."],
            ["I think I can quickly see and take advantage of new opportunities.","I have a tendency to talk a lot once the group gets on to a new topic.","I am quick to see the possibilities in new ideas and developments","I like to be the one who makes contacts outside the group or firm.","I have a chance of meeting new people with different ideas.","I would open up discussions with the view to stimulating new thoughts and getting something moving.","I tend to show boredom unless I am actively engaged with stimulating people."],
            ["My ability rests in being able to draw people out whenever I detect they have something of value to contribute to group objectives.","I am inclined to be too generous towards others who have a valid viewpoint that has not been given a proper airing","I have an aptitude for influencing people without pressurizing them.","While I am interested in hearing all views, I have no hesitation in making up my mind once a decision has to be made.","I can get people to agree on priorities.","I would find some way of reducing the size of the task by establishing how different individuals can contribute.","I am conscious of demanding from others the things I cannot do myself."],
            ["I am prepared to be blunt and outspoken in the cause of making the right things happen.","I am sometimes seen as forceful and authoritarian when dealing with important issues.","I like to press for action to make sure that the meeting does not lose sight of the main objective.","I am not reluctant to challenge the view of others or to hold a minority view myself.","I can have a strong influence on decisions.","I would take the lead if the group was making no progress.","I am apt to overreact when people hold up progress."],
            ["I can offer a reasoned and unbiased case for alternative courses of action.","My objective outlook makes it difficult for me to join in readily and enthusiastically with colleagues.","I believe my capacity for judgement can help to bring about the right decisions.","I can usually find an argument to refute unsound propositions.","I enjoy analyzing situations and weighing up all the possible choices.","I believe I would keep my cool and maintain my capacity to think straight.","Some people criticize me for being too analytical."],
            ["I can work well with a very wide range of people.","I find it difficult to lead from the front, perhaps because I am over-responsive to group atmosphere.","I am always ready to back a good suggestion in the common interest.","I maintain a quiet interest in getting to know colleagues better.","I like to feel I am fostering good working relationships.","I would be ready to work with the person who showed the most positive approach.","I find it hesitate to express my views in front of powerful or difficult people."],
            ["I can usually tell whether a plan or idea will fit a particular situation.","I am not at ease unless meetings are well structured and controlled and generally well conducted.","I can be relied on to bring an organized approach to the demands of a job.","I think I have a talent for making things work once a plan has been put into operation.","I am interested in finding practical solutions to problems.","My natural sense of urgency would help to ensure that we did not fall behind schedule.","I find it difficult to get started unless the goals are clear."],
            ["I can be relied upon to finish any task I undertake.","I am reluctant to express my opinions on proposals or plans that are incomplete or insufficiently detailed.","I am generally effective in preventing careless mistakes or omissions from spoiling the success of an operation.","I bring a touch of perfectionism to any job I undertake.","I feel I am in my element where I can give a task my full attention.","In spite of conflicting pressures I would press ahead with whatever needed to be done.","My desire to check that we get the important details right is not always welcome."],
            ["My technical knowledge and experience are usually my major assets.","I am reluctant to contribute unless the subject contains an area I know well.","I try to maintain my sense of professionalism.","I contribute where I know what I am talking about.","I feel that I am using my special qualifications and training to advantage.","I like to read up as much as I conveniently can on a subject.","I am inclined to feel I am wasting my time and would do better on my own"]
        ]
        request.session['score_array'] = [[0] * 7 for _ in range(9)]
        request.session['Roles_Score'] = [10] * 9
        request.session['Roles_List'] = ['PL', 'RI', 'CO', 'SH', 'ME', 'TW', 'IM', 'CF', 'SP']
        request.session['current_row'] = 0
        request.session['current_col'] = 0

def index(request):
    initialize_session(request)

    if request.method == "POST":
        try:
            amount_of_relativity = int(request.POST.get("score"))
            roles_score = request.session['Roles_Score']
            current_col = request.session['current_col']
            current_row = request.session['current_row']
            score_array = request.session['score_array']

            if amount_of_relativity > roles_score[current_col]:
                return JsonResponse({"error": "Please enter a smaller value!"}, status=400)
            else:
                score_array[current_row][current_col] = amount_of_relativity
                roles_score[current_col] -= amount_of_relativity
                current_row += 1
                if current_row >= 9:
                    current_row = 0
                    current_col += 1

                if current_col < 7:
                    question = request.session['questions_array'][current_row][current_col]
                    request.session['current_row'] = current_row
                    request.session['current_col'] = current_col
                    request.session['Roles_Score'] = roles_score
                    request.session['score_array'] = score_array
                    return JsonResponse({"question": question, "remaining_points": roles_score[current_col]})
                else:
                    # Calculate final scores
                    final_scores = [sum(row) for row in score_array]
                    result = dict(zip(request.session['Roles_List'], final_scores))
                    request.session.flush()  # Clear session data
                    return JsonResponse({"result": result})

        except ValueError:
            return JsonResponse({"error": "Please enter a valid number!"}, status=400)
    else:
        question = request.session['questions_array'][request.session['current_row']][request.session['current_col']]
        remaining_points = request.session['Roles_Score'][request.session['current_col']]
        return render(request, 'index.html', {'question': question, 'remaining_points': remaining_points})
