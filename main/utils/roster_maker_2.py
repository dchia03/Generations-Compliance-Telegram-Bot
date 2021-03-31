### Members are a list of [member1, member2, ...]
### Block out dates are a list of {d1: [name1, name2], .., dn:[name1, name2]}
### Hard Requirements are a list of checks for making roster
import random

from main.constants.field_names import FIELD_YEAR, FIELD_MONTH, FIELD_ROSTER, FIELD_BLOCK_OUT_DATES
from main.entity.document.impl.roster import Roster
from main.utils.logger import Logger

log = Logger(__name__)

TEAM_SIZE = 3
MAX_ITERATIONS = 200


# Hard Requirements
def can_fulfill_team_size(all_possible_assignments, all_serving_dates):
    # Check if possible to make roster given team_size
    possible_team_size_counts = {}
    for d in all_serving_dates:
        possible_team_size_counts[d] = 0

    for m, d in all_possible_assignments:
        possible_team_size_counts[d] += 1

    can_fulfill_team_size_res = True
    for d in all_serving_dates:
        can_fulfill_team_size_res &= possible_team_size_counts[d] >= TEAM_SIZE
    return can_fulfill_team_size_res


def has_one_leader_each_date(all_possible_assignments, all_serving_dates):
    # Check if there is at lease 1 leader for each week
    leaders_in_team_counts = {}
    for d in all_serving_dates:
        leaders_in_team_counts[d] = 0

    for m, d in all_possible_assignments:
        if m.is_leader():
            leaders_in_team_counts[d] += 1

    fulfill_leader_req = True
    for d in all_serving_dates:
        fulfill_leader_req &= leaders_in_team_counts[d] >= 1
    return fulfill_leader_req


def has_leader_at_date(roster, d):
    has_leader = False
    for m in roster[d]:
        has_leader |= m.is_leader()
    return has_leader


def is_serving_date_full(roster, d):
    return len(roster[d]) == TEAM_SIZE


def is_roster_complete(roster):
    res = True
    for d, member_list in roster.items():
        res &= is_serving_date_full(roster, d)
        res &= has_leader_at_date(roster, d)
    return res


def is_member_serving_in_date(roster, d, member):
    return member in roster[d]


def get_prev_roster_last_serving_week_team(prev_roster):
    if prev_roster is None or prev_roster == {}:
        return []
    all_dates = sorted(prev_roster.keys(), key=lambda x: int(x))
    return prev_roster[all_dates[-1]]


def would_serve_consecutive_dates(prev_roster, roster, d, member):
    all_dates = sorted(roster.keys())
    week_num = all_dates.index(d)
    if week_num == 0:
        return is_member_serving_in_date(roster, all_dates[week_num + 1], member) \
                or member in get_prev_roster_last_serving_week_team(prev_roster)
    elif week_num == len(all_dates) - 1:
        return is_member_serving_in_date(roster, all_dates[week_num - 1], member)
    else:
        return is_member_serving_in_date(roster, all_dates[week_num + 1], member) \
               or is_member_serving_in_date(roster, all_dates[week_num - 1], member)


def sort_possible_assigments(all_possible_assignments):
    name_count = {}
    for m, d in all_possible_assignments:
        if m.get_name() not in name_count.keys():
            name_count[m.get_name()] = 0
        name_count[m.get_name()] += 1

    possible_assignment_temp = []
    for m, d in all_possible_assignments:
        possible_assignment_temp.append([m, d, name_count[m.get_name()]])
    random.shuffle(possible_assignment_temp)
    possible_assignment_temp = sorted(possible_assignment_temp, key=lambda x: x[2])
    return [[m, d] for m, d, c in possible_assignment_temp]


def add_assignment_to_roster(roster, assignment):
    date = assignment[1]
    member = assignment[0]
    roster[date].append(member)
    return roster


def can_add_assignment_to_roster(prev_roster, roster, curr_member_assignment):
    date = curr_member_assignment[1]
    member = curr_member_assignment[0]
    is_leader = member.is_leader()
    is_serving_date_full_res = is_serving_date_full(roster, date)
    has_leader_at_date_res = has_leader_at_date(roster, date)
    is_member_serving_in_date_res = is_member_serving_in_date(roster, date, member)
    would_serve_consecutive_dates_res = would_serve_consecutive_dates(prev_roster, roster, date, member)

    if is_serving_date_full_res or is_member_serving_in_date_res:
        return False
    elif has_leader_at_date_res:
        if is_leader:
            return False
        else:
            return not would_serve_consecutive_dates_res
    else:
        if is_leader:
            return not would_serve_consecutive_dates_res
        else:
            return False


def can_add_assignment_to_roster_after_many_iterations(roster, curr_member_assignment):
    date = curr_member_assignment[1]
    member = curr_member_assignment[0]
    is_leader = member.is_leader()
    is_serving_date_full_res = is_serving_date_full(roster, date)
    has_leader_at_date_res = has_leader_at_date(roster, date)
    is_member_serving_in_date_res = is_member_serving_in_date(roster, date, member)

    if is_serving_date_full_res or is_member_serving_in_date_res:
        return False
    elif has_leader_at_date_res:
        return True
    elif is_leader:
        return True
    else:
        return False


def process_roster(roster, month, year):
    named_roster = {}
    for d in roster.keys():
        named_roster[d] = [m.get_name() for m in roster[d]]
    return Roster(month=month, year=year, roster=named_roster)


# Build Roster
def build_roster(all_members, block_out_dates_doc, prev_roster_doc):
    block_out_dates = block_out_dates_doc.get_datafield(FIELD_BLOCK_OUT_DATES)
    all_serving_dates = sorted(block_out_dates.keys(), key=lambda x: int(x))
    prev_roster = prev_roster_doc.get_datafield(FIELD_ROSTER)

    all_possible_assignments = []
    for d in all_serving_dates:
        for m in all_members:
            if m.get_name() not in block_out_dates[d]:
                all_possible_assignments.append([m, d])
    all_possible_assignments = sort_possible_assigments(all_possible_assignments)

    can_fulfill_team_size_res = can_fulfill_team_size(all_possible_assignments, all_serving_dates)

    if not can_fulfill_team_size_res:
        log.info("Unable to fulfill team size requirements given block out dates" + str(block_out_dates))
        return None, 0

    fulfill_leader_req_res = has_one_leader_each_date(all_possible_assignments, all_serving_dates)

    if not fulfill_leader_req_res:
        log.info("Unable to fulfill at least 1 Leader requirement given block out dates " + str(block_out_dates))
        return None, 0

    roster = {}
    for d in all_serving_dates:
        roster[d] = []

    curr_pos = 0
    ignore_pos = []
    while not is_roster_complete(roster) and curr_pos < MAX_ITERATIONS:
        if curr_pos not in ignore_pos:
            curr_member_assignment = all_possible_assignments[curr_pos % len(all_possible_assignments)]
            if curr_pos > MAX_ITERATIONS/2:
                can_add = can_add_assignment_to_roster_after_many_iterations(roster, curr_member_assignment)
            else:
                can_add = can_add_assignment_to_roster(prev_roster, roster, curr_member_assignment)

            if can_add:
                roster = add_assignment_to_roster(roster, curr_member_assignment)
        curr_pos += 1

    log.info("Used {} iterations to create Roster".format(curr_pos))

    roster_res = process_roster(
        roster,
        block_out_dates_doc.get_datafield(FIELD_MONTH),
        block_out_dates_doc.get_datafield(FIELD_YEAR)
    )
    return roster_res
