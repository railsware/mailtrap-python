"""Models for the Inbound Email API (folders, inboxes, messages, threads)."""

from typing import Any
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams
from mailtrap.models.mail.address import Address
from mailtrap.models.mail.attachment import Attachment

ContentDisposition = Literal["attachment", "inline"]

# --- Attachments ---


@dataclass
class InboundAttachment:
    """
    Attachment metadata on a received message. download_url and
    download_url_expires_at are only populated on get-by-id and thread responses.
    """

    attachment_id: str
    size: Optional[int] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    content_disposition: Optional[ContentDisposition] = None
    content_id: Optional[str] = None
    download_url: Optional[str] = None
    download_url_expires_at: Optional[str] = None


# --- Folders ---


@dataclass
class InboundFolder:
    id: int
    name: str


# --- Inboxes ---


@dataclass
class InboundInbox:
    id: int
    name: str
    address: str
    domain_id: int


# --- Messages ---


class InboundMessage(BaseModel):
    """A received message (list / summary shape)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    inbox_id: int
    from_: Optional[str] = Field(default=None, alias="from")
    to: list[str] = Field(default_factory=list)
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)
    reply_to: Optional[str] = None
    subject: Optional[str] = None
    rfc_message_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    references: list[str] = Field(default_factory=list)
    headers: Optional[dict[str, str]] = None
    size: Optional[int] = None
    html_size: Optional[int] = None
    text_size: Optional[int] = None
    received_at: str
    thread_id: Optional[str] = None
    attachments: list[InboundAttachment] = Field(default_factory=list)


class InboundMessageDetails(InboundMessage):
    """A received message with body and attachment download URLs (get-by-id)."""

    raw_message_url: Optional[str] = None
    raw_message_expires_at: Optional[str] = None
    html_body: Optional[str] = None
    text_body: Optional[str] = None


@dataclass
class InboundMessagesListResponse:
    """Paginated response from list messages (cursor via last_id)."""

    data: list[InboundMessage] = Field(default_factory=list)
    total_count: int = 0
    last_id: Optional[str] = None


# --- Threads ---


class InboundThreadSummary(BaseModel):
    """Thread overview (list shape and the head of a thread)."""

    id: str
    subject: Optional[str] = None
    message_count: int
    size: int
    first_message_at: str
    last_received_at: Optional[str] = None
    last_sent_at: Optional[str] = None
    last_activity_at: str
    last_message_id: Optional[str] = None
    senders: list[str] = Field(default_factory=list)
    recipients: list[str] = Field(default_factory=list)
    attachments: list[InboundAttachment] = Field(default_factory=list)


class InboundThreadMessage(BaseModel):
    """
    A message inside a thread. Only visibility_status and direction are
    guaranteed; placeholder entries omit the rest.
    """

    model_config = ConfigDict(populate_by_name=True)

    visibility_status: Literal["available", "placeholder"]
    direction: Literal["inbound", "outbound"]
    id: Optional[str] = None
    message_group_id: Optional[str] = None
    subject: Optional[str] = None
    rfc_message_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    references: Optional[list[str]] = None
    from_: Optional[str] = Field(default=None, alias="from")
    to: Optional[list[str]] = None
    cc: Optional[list[str]] = None
    bcc: Optional[list[str]] = None
    reply_to: Optional[str] = None
    created_at: Optional[str] = None
    email_size: Optional[int] = None
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    attachments: Optional[list[InboundAttachment]] = None
    delivery_status: Optional[str] = None
    delivered_at: Optional[str] = None
    bounced_at: Optional[str] = None


class InboundThread(InboundThreadSummary):
    """A thread with its messages embedded (oldest first)."""

    messages: list[InboundThreadMessage] = Field(default_factory=list)


@dataclass
class InboundThreadsListResponse:
    """Paginated response from list threads (cursor via last_id)."""

    data: list[InboundThreadSummary] = Field(default_factory=list)
    total_count: int = 0
    last_id: Optional[str] = None


@dataclass
class InboundSendResult:
    """Result of a reply, reply-all, or forward (sends a real email)."""

    message_ids: list[str] = Field(default_factory=list)


# --- Request params ---


@dataclass
class CreateInboundFolderParams(RequestParams):
    name: str


@dataclass
class UpdateInboundFolderParams(RequestParams):
    name: str


@dataclass
class CreateInboundInboxParams(RequestParams):
    """Omit domain_id for a Mailtrap-hosted inbox; pass it for a custom-domain inbox."""

    name: str
    domain_id: Optional[int] = None


@dataclass
class UpdateInboundInboxParams(RequestParams):
    name: str


@dataclass
class _InboundMessageParams(RequestParams):
    """
    Shared body for replying to and forwarding an inbound message. `sender`
    (serialized as `from`) is rejected for Mailtrap-hosted inboxes and required
    for custom-domain inboxes.
    """

    sender: Optional[Address] = Field(default=None, serialization_alias="from")
    to: Optional[list[Address]] = None
    cc: Optional[list[Address]] = None
    bcc: Optional[list[Address]] = None
    reply_to: Optional[Address] = None
    text: Optional[str] = None
    html: Optional[str] = None
    category: Optional[str] = None
    attachments: Optional[list[Attachment]] = None
    headers: Optional[dict[str, str]] = None
    custom_variables: Optional[dict[str, Any]] = None


@dataclass
class ReplyInboundMessageParams(_InboundMessageParams):
    """Body for replying to (or reply-all-ing) an inbound message."""


@dataclass
class ForwardInboundMessageParams(_InboundMessageParams):
    """Forward an inbound message; requires at least one recipient in `to`."""

    to: list[Address] = Field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.to:
            raise ValueError("`to` must contain at least one recipient for forward")
