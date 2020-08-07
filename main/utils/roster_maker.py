import random

from main.constants.field import *
from main.database.roster import Roster


def split_leaders_and_members(all_members):
    leaders = []
    members = []
    for m in all_members:
        if m.get_datafield(FIELD_ROLE) == ROLE_MEMBER:
            members.append(m)
        else:
            leaders.append(m)
    return leaders, members


def sort_block_out_dates_priority(members, block_out_dates):
    members_num_block_out_dates = []
    for m in members:
        num_block_out_dates = 0
        for d in list(block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES).keys()):
            if m.get_datafield(FIELD_NAME) in block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES)[d]:
                num_block_out_dates += 1
        members_num_block_out_dates.append([m, num_block_out_dates])
    members_num_block_out_dates = sorted(
        members_num_block_out_dates,
        reverse=True,
        key=lambda x: x[1]
    )
    return [m[0] for m in members_num_block_out_dates]


def has_a_leader(serving_week):
    for m in serving_week:
        if not m.get_datafield(FIELD_ROLE) == ROLE_MEMBER:
            return True
    return False


def is_serving_week_full(serving_week, min_serve_members):
    return len(serving_week) >= min_serve_members


def has_a_leader_in_all_weeks(roster):
    res = True
    for d in list(roster.get_datafield(FIELD_ROSTER).keys()):
        res &= has_a_leader(roster.get_datafield(FIELD_ROSTER)[d])
    return res


def is_roster_full(roster, min_serve_members):
    res = True
    for d in list(roster.get_datafield(FIELD_ROSTER).keys()):
        res &= is_serving_week_full(roster.get_datafield(FIELD_ROSTER)[d], min_serve_members)
    return res


def get_person_serving_amount(roster, person):
    return sum([1 for d in roster.get_datafield(FIELD_ROSTER).keys() if
                person.get_datafield(FIELD_NAME) in roster.get_datafield(FIELD_ROSTER)[d]])


def get_avg_serving_amount(roster, persons):
    return sum([get_person_serving_amount(roster, person) for person in persons]) / len(persons)


def process_new_roster(roster):
    schedule = {}
    for d in sorted(roster.get_datafield(FIELD_ROSTER).keys(), key=lambda x: int(x)):
        schedule[d] = [member.get_datafield(FIELD_NAME) for member in roster.get_datafield(FIELD_ROSTER)[d]]
    roster.set_datafield(field=FIELD_ROSTER, data=schedule)
    return roster


def roster_maker(block_out_dates, all_members, prev_roster, min_serve_members=3):
    last_month_serving_week = []
    if prev_roster != {}:
        last_month_date = sorted(
            prev_roster.get_datafield(FIELD_ROSTER).keys(),
            key=lambda x: int(x)
        )[-1]
        last_month_serving_week = prev_roster.get_datafield(FIELD_ROSTER)[last_month_date]
    serving_dates = sorted(
        block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES).keys(),
        key=lambda x: int(x)
    )
    serving_members = []
    for m in all_members:
        can_serve = False
        for d in list(block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES).keys()):
            if m.get_datafield(FIELD_NAME) not in block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES)[d]:
                can_serve |= True
        if can_serve:
            serving_members.append(m)
    roster = Roster(
        month=str(block_out_dates.get_datafield(FIELD_MONTH)),
        year=int(block_out_dates.get_datafield(FIELD_YEAR))
    )
    schedule = {}
    for d in serving_dates:
        schedule[d] = []
    roster.set_datafield(field=FIELD_ROSTER, data=schedule)
    random.shuffle(serving_members)
    all_members = sort_block_out_dates_priority(serving_members, block_out_dates)
    one_time_leaders, one_time_members = split_leaders_and_members(all_members)
    iteration_counts = 0
    is_too_many_iterations = False
    while (len(one_time_leaders) > 0 or len(one_time_members) > 0) and (not is_too_many_iterations):
        iteration_counts += 1
        is_too_many_iterations = iteration_counts > 20
        if is_roster_full(roster, min_serve_members):
            break
        else:
            for d in range(len(serving_dates)):
                date = serving_dates[d]
                is_first_date = d == 0
                is_last_date = d == len(serving_dates) - 1
                has_more_than_one_slot_left = (min_serve_members - len(roster.get_datafield(FIELD_ROSTER)[date])) > 1
                still_has_members = len(one_time_members) > 0
                still_has_leaders = len(one_time_leaders) > 0
                is_member_available = still_has_members and (
                    one_time_members[0].get_datafield(FIELD_NAME) not in
                    block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES)[date]
                )
                is_leader_available = still_has_leaders \
                    and (
                        one_time_leaders[0].get_datafield(FIELD_NAME) not in
                        block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES)[date]
                    )
                is_member_in_prev_week = still_has_members \
                    and (
                        (is_first_date and (one_time_members[0].get_datafield(FIELD_NAME) in last_month_serving_week))
                        or (
                            (not is_first_date)
                            and (
                                one_time_members[0].get_datafield(FIELD_NAME) in
                                roster.get_datafield(FIELD_ROSTER)[serving_dates[d - 1]]
                            )
                        )
                    )
                is_member_in_next_week = still_has_members \
                    and (
                        (is_last_date and (one_time_members[0].get_datafield(FIELD_NAME) in []))
                        or (
                            (not is_last_date)
                            and (one_time_members[0].get_datafield(FIELD_NAME) in roster.get_datafield(FIELD_ROSTER)[serving_dates[d + 1]])
                        )
                    )
                is_leader_in_prev_week = still_has_leaders \
                    and (
                        (
                            is_first_date and (one_time_leaders[0].get_datafield(FIELD_NAME) in last_month_serving_week)
                        ) or (
                            (not is_first_date)
                            and (one_time_leaders[0].get_datafield(FIELD_NAME) in roster.get_datafield(FIELD_ROSTER)[serving_dates[d - 1]])
                        )
                    )
                is_leader_in_next_week = still_has_leaders \
                    and (
                        (is_last_date and (one_time_leaders[0].get_datafield(FIELD_NAME) in []))
                        or (
                            (not is_last_date)
                            and (one_time_leaders[0].get_datafield(FIELD_NAME) in roster.get_datafield(FIELD_ROSTER)[serving_dates[d + 1]])
                        )
                    )
                if not is_serving_week_full(roster.get_datafield(FIELD_ROSTER)[date], min_serve_members):
                    if not has_a_leader(roster.get_datafield(FIELD_ROSTER)[date]):
                        if still_has_leaders:
                            if not is_leader_in_prev_week and not is_leader_in_next_week and is_leader_available:
                                roster.get_datafield(FIELD_ROSTER)[date].append(one_time_leaders.pop(0))
                            else:
                                print(one_time_leaders[0].get_datafield(FIELD_NAME),
                                      'is in prev or next serving week. Date:', date)
                        else:
                            if has_more_than_one_slot_left:
                                if still_has_members:
                                    if not is_member_in_prev_week and not is_member_in_next_week and is_member_available:
                                        roster.get_datafield(FIELD_ROSTER)[date].append(one_time_members.pop(0))
                                    else:
                                        print(one_time_members[0].get_datafield(FIELD_NAME),
                                              'is in prev or next serving week. Date:', date)
                                else:
                                    print('Not enough members to roster. Date:', date)
                            else:
                                print('Serving date almost full with one slot left for a leader. Date:', date)
                    else:
                        if still_has_members:
                            if not is_member_in_prev_week and not is_member_in_next_week and is_member_available:
                                roster.get_datafield(FIELD_ROSTER)[date].append(one_time_members.pop(0))
                            else:
                                print(one_time_members[0].get_datafield(FIELD_NAME),
                                      'is in prev or next serving week. Date:', date)
                        elif still_has_leaders:
                            if not is_leader_in_prev_week and not is_leader_in_next_week and is_leader_available:
                                roster.get_datafield(FIELD_ROSTER)[date].append(one_time_leaders.pop(0))
                            else:
                                print(one_time_leaders[0].get_datafield(FIELD_NAME),
                                      'is in prev or next serving week. Date:', date)
                        else:
                            print('All members and leaders rostered at least once. Date:', date)

    iteration_counts = 0
    while not is_roster_full(roster, min_serve_members):
        for person in serving_members:
            for d in range(len(serving_dates)):
                is_many_iterations = iteration_counts > 10
                is_too_many_iterations = iteration_counts > 20
                date = serving_dates[d]
                is_first_date = d == 0
                is_last_date = d == len(serving_dates) - 1
                has_more_than_one_slot_left = min_serve_members - len(roster.get_datafield("Roster")[date]) > 1
                is_member = person.get_datafield(FIELD_ROLE) == ROLE_MEMBER
                is_leader = not is_member
                is_person_available = person.get_datafield(FIELD_NAME) not in \
                                      block_out_dates.get_datafield(FIELD_BLOCK_OUT_DATES)[date] and person not in \
                                      roster.get_datafield(FIELD_ROSTER)[date]
                is_member_in_prev_week = is_member and (
                        (is_first_date and (person.get_datafield(FIELD_NAME) in last_month_serving_week)) or (
                        (not is_first_date) and (
                        person in roster.get_datafield(FIELD_ROSTER)[serving_dates[d - 1]])))
                is_member_in_next_week = is_member and ((is_last_date and (person.get_datafield(FIELD_NAME) in [])) or (
                        (not is_last_date) and (person in roster.get_datafield(FIELD_ROSTER)[serving_dates[d + 1]])))
                is_leader_in_prev_week = is_leader and (
                        (is_first_date and (person.get_datafield(FIELD_NAME) in last_month_serving_week)) or (
                        (not is_first_date) and (
                        person in roster.get_datafield(FIELD_ROSTER)[serving_dates[d - 1]])))
                is_leader_in_next_week = is_leader and ((is_last_date and (person.get_datafield(FIELD_NAME) in [])) or (
                        (not is_last_date) and (person in roster.get_datafield(FIELD_ROSTER)[serving_dates[d + 1]])))
                is_serve_too_much = get_person_serving_amount(roster, person) > get_avg_serving_amount(roster,
                                                                                                       serving_members)

                if is_person_available and not is_serving_week_full(
                        roster.get_datafield(FIELD_ROSTER)[date],
                        min_serve_members
                ):
                    if not has_a_leader(roster.get_datafield(FIELD_ROSTER)[date]):
                        if is_leader \
                            and (
                                (not is_leader_in_prev_week and not is_leader_in_next_week)
                                or (is_many_iterations and not is_serve_too_much)
                                or is_too_many_iterations
                        ):
                            roster.get_datafield(FIELD_ROSTER)[date].append(person)
                            break
                    else:
                        if (is_member and is_member_in_prev_week and is_member_in_next_week) or (
                                is_leader and not is_leader_in_prev_week and not is_leader_in_next_week) or (
                                is_many_iterations and not is_serve_too_much) or is_too_many_iterations:
                            roster.get_datafield(FIELD_ROSTER)[date].append(person)
                            break
        iteration_counts += 1
    roster = process_new_roster(roster)
    print(sorted(
        [(person.get_datafield(FIELD_NAME), get_person_serving_amount(roster, person)) for person in serving_members],
        key=lambda x: x[1], reverse=True))
    print(roster.get_roster_str())
    return roster
