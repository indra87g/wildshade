use tracing_subscriber::{fmt, prelude::*, Registry};
use tracing_subscriber::fmt::format::FmtSpan;

pub fn init() {
    let fmt_layer = fmt::layer()
        .with_span_events(FmtSpan::CLOSE)
        .with_target(false);

    let subscriber = Registry::default().with(fmt_layer);
    tracing::subscriber::set_global_default(subscriber).expect("failed to set up logger");
}

pub fn log_info(msg: &str) {
    tracing::info!("{}", msg);
}

pub fn log_warning(msg: &str) {
    tracing::warn!("{}", msg);
}
