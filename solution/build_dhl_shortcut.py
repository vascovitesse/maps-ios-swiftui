import plistlib
from collections import OrderedDict
from pathlib import Path


def token_string(text: str, attachments: OrderedDict | None = None):
    payload: dict[str, object] = {
        "Type": "WFVariableSubstitutableString",
        "Value": {"string": text},
    }
    if attachments:
        payload["Value"]["attachmentsByRange"] = {
            f"{{{start}, {length}}}": {
                "Type": "WFVariableAttachment",
                "VariableName": variable,
            }
            for (start, length), variable in attachments.items()
        }
    return {
        "WFSerializationType": "WFTextTokenString",
        "Value": payload,
    }


def variable_token(name: str):
    length = len(name)
    return token_string(name, OrderedDict([((0, length), name)]))


def choose_from_menu(prompt, items):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefrommenu",
        "WFWorkflowActionParameters": {
            "WFMenuPrompt": prompt,
            "WFMenuItems": [
                {
                    "WFMenuItemTitle": title,
                    "WFMenuItemSubWorkflow": {"WFWorkflowActions": subactions},
                }
                for title, subactions in items
            ],
        },
    }


def ask_for_input(prompt, input_type="Text"):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.ask",
        "WFWorkflowActionParameters": {
            "WFAskActionPrompt": prompt,
            "WFAskActionInputType": input_type,
        },
    }


def set_variable(name):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.setvariable",
        "WFWorkflowActionParameters": {"WFVariableName": name},
    }


def get_variable(name):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getvariable",
        "WFWorkflowActionParameters": {"WFVariableName": name},
    }


def text_action(value):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.text",
        "WFWorkflowActionParameters": {"WFTextActionText": value},
    }


def text_with_variable(template: str, variable: str):
    start = template.index(variable)
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.text",
        "WFWorkflowActionParameters": {
            "WFTextActionText": token_string(
                template,
                OrderedDict([((start, len(variable)), variable)]),
            )
        },
    }


def url_with_variable(prefix: str, variable: str):
    start = len(prefix)
    template = prefix
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.url",
        "WFWorkflowActionParameters": {
            "WFURLActionURL": token_string(
                template,
                OrderedDict([((start, 0), variable)]),
            )
        },
    }


def open_url_action():
    return {"WFWorkflowActionIdentifier": "is.workflow.actions.openurl"}


workflow = {
    "WFWorkflowName": "DHL Tracker",
    "WFWorkflowClientRelease": "2000",
    "WFWorkflowClientVersion": "1000",
    "WFWorkflowTypes": ["WatchKit", "NCWidget", "ActionExtension"],
    "WFWorkflowIcon": {
        "WFWorkflowIconGlyphNumber": 59773,
        "WFWorkflowIconStartColor": 0xFFCC00FF,
        "WFWorkflowIconImageData": b"",
    },
}

actions: list[dict] = []


pick_favorite_actions = [
    {
        "WFWorkflowActionIdentifier": "is.workflow.actions.findreminders",
        "WFWorkflowActionParameters": {
            "WFReminderList": "DHL Tracking Favorites",
            "WFReminderCompleted": False,
            "WFReminderSearchAll": True,
        },
    },
    set_variable("Favorite Reminders"),
    get_variable("Favorite Reminders"),
    {"WFWorkflowActionIdentifier": "is.workflow.actions.count"},
    {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "WFCondition": "Number",
            "WFConditionalAction": "Equals",
            "WFConditionalActionNumber": 0,
        },
        "WFConditionalActionTrueSubWorkflow": {
            "WFWorkflowActions": [
                {
                    "WFWorkflowActionIdentifier": "is.workflow.actions.showalert",
                    "WFWorkflowActionParameters": {
                        "WFAlertActionTitle": "No favorites saved yet. Pick \"Track New\" instead.",
                        "WFAlertActionStyle": "Alert",
                    },
                },
                {"WFWorkflowActionIdentifier": "is.workflow.actions.exit"},
            ]
        },
    },
    get_variable("Favorite Reminders"),
    {
        "WFWorkflowActionIdentifier": "is.workflow.actions.choosefromlist",
        "WFWorkflowActionParameters": {
            "WFChooseFromListActionPrompt": "Select a saved shipment",
        },
    },
    {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getdetails.reminders",
        "WFWorkflowActionParameters": {
            "WFGetDetailsActionProperty": "Notes",
        },
    },
    set_variable("Tracking Number"),
    text_action("favorite"),
    set_variable("Tracking Mode"),
]

track_new_actions = [
    ask_for_input("Enter your DHL tracking number"),
    set_variable("Tracking Number"),
    text_action("new"),
    set_variable("Tracking Mode"),
]

actions.append(
    choose_from_menu(
        "How do you want to track?",
        [
            ("Pick Favorite", pick_favorite_actions),
            ("Track New", track_new_actions),
        ],
    )
)

actions.append(
    choose_from_menu(
        "Select the DHL service",
        [
            (
                "Express",
                [
                    url_with_variable(
                        "https://www.dhl.com/global-en/home/tracking/tracking-express.html?submit=1&tracking-id=",
                        "Tracking Number",
                    ),
                    open_url_action(),
                ],
            ),
            (
                "Parcel & eCommerce",
                [
                    url_with_variable(
                        "https://www.dhl.com/global-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=",
                        "Tracking Number",
                    ),
                    open_url_action(),
                ],
            ),
        ],
    )
)

actions.extend(
    [
        get_variable("Tracking Mode"),
        {
            "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
            "WFWorkflowActionParameters": {
                "WFCondition": "String",
                "WFConditionalAction": "Equals",
                "WFConditionalActionString": "new",
            },
            "WFConditionalActionTrueSubWorkflow": {
                "WFWorkflowActions": [
                    choose_from_menu(
                        "Save this tracking number as a favorite?",
                        [
                            (
                                "Yes",
                                [
                                    ask_for_input(
                                        "Give this favorite a short name (e.g., \"Laptop Repair\")"
                                    ),
                                    set_variable("Favorite Label"),
                                    {
                                        "WFWorkflowActionIdentifier": "is.workflow.actions.addnewreminder",
                                        "WFWorkflowActionParameters": {
                                            "WFReminderTitle": variable_token("Favorite Label"),
                                            "WFReminderNotes": variable_token("Tracking Number"),
                                            "WFReminderList": "DHL Tracking Favorites",
                                        },
                                    },
                                ],
                            ),
                            ("No", []),
                        ],
                    )
                ]
            },
        },
    ]
)

workflow["WFWorkflowActions"] = actions

output_path = Path(__file__).resolve().parents[1] / "shortcuts" / "DHL_Tracker.shortcut"
with output_path.open("wb") as fp:
    plistlib.dump(workflow, fp)

print(f"Wrote shortcut to {output_path}")
