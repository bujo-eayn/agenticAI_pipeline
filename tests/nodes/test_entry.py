import os
import pytest
from unittest.mock import patch, MagicMock
from graph.nodes.entry import entry_node

DUMMY_CONTEXT = "This is dummy context data to be used when the user provides only a prompt."


@pytest.fixture
def tmp_text_file(tmp_path):
    file_path = tmp_path / "test_doc.txt"
    file_content = "This is a test document."
    file_path.write_text(file_content, encoding="utf-8")
    return str(file_path), file_content


@patch("graph.nodes.entry.logger")
def test_entry_node_with_prompt_only(mock_logger):
    state = {
        "user_prompt": "Summarize the following text."
    }
    result = entry_node(state)
    assert result["input_type"] == "prompt_only"
    assert result["dummy_context"] == DUMMY_CONTEXT
    mock_logger.info.assert_any_call(
        "Executing entry_node with state: %s", state)
    mock_logger.info.assert_any_call(
        "entry_node completed with state: %s", result)


@patch("graph.nodes.entry.logger")
def test_entry_node_with_file_only(mock_logger, tmp_text_file):
    file_path, file_content = tmp_text_file
    state = {
        "file_path": file_path
    }
    result = entry_node(state)
    assert result["input_type"] == "file_or_both"
    assert result["file_content"] == file_content
    mock_logger.info.assert_any_call(
        "File read successfully, length: %d", len(file_content))
    mock_logger.info.assert_any_call(
        "entry_node completed with state: %s", result)


@patch("graph.nodes.entry.logger")
def test_entry_node_with_both_prompt_and_file(mock_logger, tmp_text_file):
    file_path, file_content = tmp_text_file
    state = {
        "user_prompt": "Analyze this document.",
        "file_path": file_path
    }
    result = entry_node(state)
    assert result["input_type"] == "file_or_both"
    assert result["file_content"] == file_content
    assert "dummy_context" not in result
    mock_logger.info.assert_any_call(
        "Executing entry_node with state: %s", state)


@patch("graph.nodes.entry.logger")
def test_entry_node_raises_error_on_empty_input(mock_logger):
    state = {
        "user_prompt": "",
        "file_path": ""
    }
    with pytest.raises(ValueError, match="No prompt or document provided."):
        entry_node(state)
    mock_logger.info.assert_any_call(
        "Executing entry_node with state: %s", state)


@patch("graph.nodes.entry.logger")
def test_entry_node_raises_file_not_found(mock_logger):
    state = {
        "file_path": "nonexistent_file.txt"
    }
    with pytest.raises(FileNotFoundError, match="No file found in the state."):
        entry_node(state)
    mock_logger.error.assert_called_once()
