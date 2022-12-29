import mock

from data_handler.main import run_handler


def test_run_handler(args, config):
    mock_data_saver = mock.MagicMock()
    with mock.patch('data_handler.main.init_kafka_consumer'), \
            mock.patch('data_handler.main.init_data_saver', return_value=mock_data_saver), \
            mock.patch('data_handler.main._run_endless_loop'):
        run_handler(args, config)

        assert mock.call.init() in mock_data_saver.method_calls
        assert mock.call.finalize() in mock_data_saver.method_calls
